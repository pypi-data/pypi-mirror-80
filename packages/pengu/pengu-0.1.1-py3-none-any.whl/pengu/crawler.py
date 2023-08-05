import json
import re
import io
from pathlib import Path
from six.moves.urllib.parse import urlparse
from typing import Dict, Any, List, Tuple

import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
from icrawler.builtin.google import GoogleParser
from icrawler import ImageDownloader
from sklearn.model_selection import train_test_split

from pengu.data.image_utils import get_image_meta


class ImagesDataCSV(object):
    DELIMITER = ","
    URL_COL: str = "url"
    FILE_PATH_COL: str = "file_path"
    LABEL_COL: str = "label"
    IMG_W_COL: str = "img_w"
    IMG_H_COL: str = "img_h"
    MODE_COL: str = "mode"
    HASH_COL: str = "hash"
    FORMAT_COL: str = "format"
    HEADER: List[str] = [URL_COL, FILE_PATH_COL, LABEL_COL,
                         IMG_W_COL, IMG_H_COL, MODE_COL,
                         HASH_COL, FORMAT_COL]

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path

    @classmethod
    def write_header(cls, csv_path: Path):
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            f.write(cls.DELIMITER.join(cls.HEADER) + "\n")

    def write_row(self,
                  url: str,
                  file_path: str,
                  label: str,
                  img_w: str,
                  img_h: str,
                  mode: str,
                  hash: str,
                  format: str):
        row: List[str] = [url, file_path, label, img_w, img_h, mode, hash, format]
        with open(self.csv_path, 'a', newline='') as f:
            f.write(self.DELIMITER.join(row) + "\n")

    def drop_duplicates_hash(self) -> None:
        df = pd.read_csv(self.csv_path)
        df = df.drop_duplicates(subset=[self.HASH_COL], keep="first")
        self.df = df

    def split_train_val_test(
            self,
            ratio: Tuple[float, float, float]) -> Tuple[pd.DataFrame,
                                                        pd.DataFrame,
                                                        pd.DataFrame]:
        train_ratio, val_ratio, test_ratio = ratio
        df = self.df[[self.FILE_PATH_COL, self.LABEL_COL]]
        labels = df[self.LABEL_COL]
        train_val_df, test_df, _, _ = train_test_split(
            df, labels, test_size=test_ratio, random_state=0, stratify=labels
        )
        train_val_labels = train_val_df[self.LABEL_COL]
        test_size = val_ratio / (train_ratio + val_ratio)
        train_df, val_df, _, _ = train_test_split(
            train_val_df, train_val_labels,
            test_size=test_size, random_state=0, stratify=train_val_labels
        )
        return train_df, val_df, test_df


class SaveResultImageDownloader(ImageDownloader):
    def __init__(self, thread_num, signal, session, storage,
                 image_data_csv_path: Path,
                 label: str,
                 image_exts: List[str] = ["jpeg", "jpg", "png"]):
        """Init Parser with some shared variables."""
        super(SaveResultImageDownloader, self).__init__(
            thread_num, signal, session, storage)

        image_data_csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.image_data_csv = ImagesDataCSV(csv_path=image_data_csv_path)
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

            self.image_data_csv.write_row(
                url=url, file_path=file_path, label=self.label,
                img_w=str(img_w), img_h=str(img_h), mode=img_mode,
                hash=str(img_hash), format=img_format)

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
            txt = re.sub(r"^AF_initDataCallback\({.*key: 'ds:(\d)'.+data:(.+)}\);?$",
                         "\\2", txt, 0, re.DOTALL)

            meta = json.loads(txt)
            data = meta[31][0][12][2]

            uris = [img[1][3][0] for img in data if img[0] == 1]
            return [{'file_url': uri} for uri in uris]
