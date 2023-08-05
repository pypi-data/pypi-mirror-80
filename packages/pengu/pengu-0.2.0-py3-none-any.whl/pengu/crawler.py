import json
import re
import io
from pathlib import Path
from six.moves.urllib.parse import urlparse
from typing import Dict, Any, List

from PIL import Image
from bs4 import BeautifulSoup
from icrawler.builtin.google import GoogleParser
from icrawler import ImageDownloader

from pengu.data.image_utils import get_image_meta
from pengu.core.csv_core import ImagesDataCSV, ImageUrlCSV


class SaveUrlNotDownloadDownloader(ImageDownloader):
    def __init__(self, thread_num, signal, session, storage,
                 csv_path: Path,
                 label: str):
        """"""
        super(SaveUrlNotDownloadDownloader, self).__init__(
            thread_num, signal, session, storage)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv = ImageUrlCSV(csv_path=csv_path)
        self.label = label

    def download(self,
                 task,
                 default_ext,
                 timeout=5,
                 max_retry=3,
                 overwrite=False,
                 **kwargs):
        """Not download and write [url, label] (in self.process_meta).
        Override icrawler.downloader.Downloader.download method.
        """
        task['success'] = True

    def process_meta(self, task: Dict[str, Any]):
        if task.get("success"):
            _url = task.get("file_url", "")
            url: str = _url if isinstance(_url, str) else ""
            row: List[str] = [url, self.label]
            self.csv.write_row(row)


class SaveResultImageDownloader(ImageDownloader):
    def __init__(self, thread_num, signal, session, storage,
                 csv_path: Path,
                 label: str,
                 image_exts: List[str] = ["jpeg", "jpg", "png"]):
        """Init Parser with some shared variables."""
        super(SaveResultImageDownloader, self).__init__(
            thread_num, signal, session, storage)

        csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv = ImagesDataCSV(csv_path=csv_path)
        self.label = label
        self.image_exts = image_exts

    def process_meta(self, task: Dict[str, Any]):
        if task.get("success"):
            _url = task.get("file_url", "")
            url: str = _url if isinstance(_url, str) else ""
            _file_name = task.get("filename", "")
            file_name: str = _file_name if isinstance(_file_name, str) else ""
            storage_dir: Path = Path(self.storage.root_dir)
            keyword_dir: str = str(storage_dir.name).replace(" ", "_")
            file_path: str = f"{keyword_dir}/{file_name}"
            img_w, img_h = task["img_size"]
            img_mode = task["img_mode"]
            img_hash = task["img_hash"]
            img_format = task["img_format"]

            row: List[str] = [url, file_path, self.label, str(img_w),
                              str(img_h), img_mode, str(img_hash), img_format]
            self.csv.write_row(row)

    def keep_file(self, task, response, min_size=None, max_size=None):
        """Decide whether to keep the image & add hash
        Compare image size with ``min_size`` and ``max_size`` to decide.

        Args:
            response (Response): response of requests.
            min_size (tuple or None): minimum size of required images.
            max_size (tuple or None): maximum size of required images.

        Returns:
            bool: whether to keep the image.
        """
        try:
            img = Image.open(io.BytesIO(response.content))
        except (IOError, OSError):
            return False
        img_size, img_mode, img_hash, img_format \
            = get_image_meta(img, data_format="pil", hash_method="phash")
        task["img_size"] = img_size
        task["img_mode"] = img_mode
        task["img_hash"] = img_hash
        task["img_format"] = img_format

        if min_size and not self._size_gt(img.size, min_size):
            return False
        if max_size and not self._size_lt(img.size, max_size):
            return False
        return True

    def get_filename(self, task, default_ext):
        url_path = urlparse(task['file_url'])[2]
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in self.image_exts:
                extension = default_ext
        else:
            extension = default_ext
        file_idx = self.fetched_num + self.file_idx_offset
        return '{:06d}.{}'.format(file_idx, extension)

    def worker_exec(self,
                    max_num,
                    default_ext='jpg',
                    queue_timeout=5,
                    req_timeout=5,
                    **kwargs):
        default_req_timeout: int = 1
        default_queue_timeout: int = 1
        super(SaveResultImageDownloader, self).worker_exec(
            max_num, default_ext, queue_timeout=default_queue_timeout,
            req_timeout=default_req_timeout, max_retry=1)


class FixedGoogleParser(GoogleParser):
    def parse(self, response):
        soup = BeautifulSoup(
            response.content.decode('utf-8', 'ignore'), 'lxml')
        image_divs = soup.find_all('script')
        for div in image_divs:
            txt = div.string
            if txt is None or not txt.startswith('AF_initDataCallback'):
                continue
            if 'ds:1' not in txt:
                continue
            # https://github.com/hellock/icrawler/pull/74
            txt = re.sub(r"^AF_initDataCallback\({.*key: 'ds:(\d)'.+data:(.+), "
                         r"sideChannel: {}}\);?$",
                         "\\2", txt, 0, re.DOTALL)

            meta = json.loads(txt)
            data = meta[31][0][12][2]

            uris = [img[1][3][0] for img in data if img[0] == 1]
            return [{'file_url': uri} for uri in uris]
