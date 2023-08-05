from __future__ import annotations

import io
import queue
import threading
import logging
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, astuple
from queue import Queue
from typing import DefaultDict, Optional, Tuple, List

import requests
from PIL import Image
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from pengu.core.csv_core import ImageDataRowItem, ImageUrlCSV, ImagesDataCSV
from pengu.data.image_utils import get_image_meta, resize_image
from pengu.exceptions import DownloadError


def create_retry_session(retry_count: int = 3,
                         retry_backoff_factor: float = 0.5) -> requests.Session:
    session = requests.Session()

    retries = Retry(total=retry_count,
                    backoff_factor=retry_backoff_factor)

    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


def download_image(url: str,
                   timeout: float = 1.0,
                   session: Optional[requests.Session] = None) -> Image.Image:
    """Download Image from image url

    Args:
        url (str): image url

    Raises:
        DownloadError

    Returns:
        Image.Image: PIL Image.
    """
    if session is None:
        session = requests.Session()

    try:
        response = session.get(url, timeout=timeout)
    except requests.exceptions.ConnectionError as e:
        raise DownloadError(f"Max retries exceeded with url({url})") from e

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise DownloadError(f"Failed to download Image. url: {url}") from e
    except requests.exceptions.Timeout as e:
        raise DownloadError("Downloading timed out") from e

    try:
        img = Image.open(io.BytesIO(response.content))
    except OSError as e:
        raise DownloadError(f"Failed to open image downloaded. url: {url}") from e

    return img


class ImageDownloadThread(threading.Thread):
    @dataclass
    class UrlItem:
        url: str
        label: str
        file_name_no_ext: str

    def __init__(self,
                 url_queue: Queue[ImageDownloadThread.UrlItem],
                 result_queue: Queue[ImageDataRowItem],
                 session: requests.Session,
                 timeout: float,
                 resize_max_size: Tuple[int, int]):
        super(ImageDownloadThread, self).__init__()
        self.url_queue: Queue[ImageDownloadThread.UrlItem] = url_queue
        self.result_queue: Queue[ImageDataRowItem] = result_queue
        self.session = session
        self.timeout = timeout
        self.resize_max_size = resize_max_size

    def run(self):
        while True:
            item: ImageDownloadThread.UrlItem = self.url_queue.get()

            try:
                img = download_image(item.url,
                                     timeout=self.timeout,
                                     session=self.session)
            except DownloadError:
                result_item = ImageDataRowItem(
                    url=item.url, file_path="", label=item.label,
                    img_w="", img_h="", mode="", hash_str="", format_str="")
                self.result_queue.put(result_item)
                self.url_queue.task_done()
                continue

            (img_w, img_h), img_mode, img_hash, img_format \
                = get_image_meta(img, data_format="pil", hash_method="phash")
            resized_img = resize_image(img, size=self.resize_max_size, preserve_aspect_ratio=True)
            if resized_img.mode != "RGB":
                resized_img = resized_img.convert("RGB")
            file_path = item.file_name_no_ext + ".jpg"
            Path(file_path).parent.mkdir(exist_ok=True, parents=True)
            resized_img.save(file_path, format="JPEG")

            image_item: ImageDataRowItem = ImageDataRowItem(
                url=item.url, file_path=file_path, label=item.label,
                img_w=str(img_w), img_h=str(img_h), mode=img_mode,
                hash_str=str(img_hash), format_str=img_format
            )
            self.result_queue.put(image_item)
            self.url_queue.task_done()


class ImageDownloader:
    LOG_INTERVAL: int = 1000

    def __init__(self,
                 n_workers: int,
                 resize_max_size: Tuple[int, int],
                 retry_count: int,
                 retry_backoff_factor: float,
                 timeout: float):
        self._n_workers = n_workers
        self._resize_max_size = resize_max_size
        self._session = create_retry_session(
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor
        )
        self._timeout = timeout

        self._url_queue: Queue[ImageDownloadThread.UrlItem] = Queue()
        self._result_queue: Queue[ImageDataRowItem] = Queue()

    def _init_workers(self):
        self._workers = []
        for i in range(self._n_workers):
            download_thread = ImageDownloadThread(
                url_queue=self._url_queue,
                result_queue=self._result_queue,
                session=self._session,
                timeout=self._timeout,
                resize_max_size=self._resize_max_size
            )
            self._workers.append(download_thread)

    def _start(self):
        for worker in self._workers:
            worker.start()
            logging.debug(f"Thread {worker.name} started")

    def _terminate(self):
        for worker in self._workers:
            worker.join()
            logging.info(f"Terminate {worker.name} thread")

    def _write_result(self, img_data_csv: ImagesDataCSV) -> None:
        while True:
            try:
                row_item: ImageDataRowItem = self._result_queue.get_nowait()
            except queue.Empty:
                break
            row: List[str] = astuple(row_item)  # type: ignore
            img_data_csv.write_row(row)

    def download(self,
                 url_csv: ImageUrlCSV,
                 img_dir: Path,
                 img_data_csv: ImagesDataCSV):
        img_dir.mkdir(parents=True, exist_ok=True)
        self._init_workers()
        self._start()
        label2count: DefaultDict[str, int] = defaultdict(int)
        n_row: int = len(url_csv)

        for i, (url, label) in enumerate(url_csv.get_row_data_geenrator()):
            label2count[label] += 1
            count = label2count[label]
            file_path_no_ext = str(img_dir / label / f"{count:07}")
            item = ImageDownloadThread.UrlItem(
                url=url, label=label, file_name_no_ext=file_path_no_ext)
            self._url_queue.put(item)

            if i % self.LOG_INTERVAL == 0:
                logging.info(f"[{i}/{n_row}] Download {i} images")

        self._url_queue.join()
        self._write_result(img_data_csv)
        self._terminate()
