import abc
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Generator

import six
import pandas as pd
from sklearn.model_selection import train_test_split


@six.add_metaclass(abc.ABCMeta)
class BaseCSV(object):
    DELIMITER: str = ","
    HEADER: List[str] = [""]

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path

    @classmethod
    def write_header(cls, csv_path: Path):
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            f.write(cls.DELIMITER.join(cls.HEADER) + "\n")

    def write_row(self, row: List[str]):
        with open(self.csv_path, 'a', newline='') as f:
            f.write(self.DELIMITER.join(row) + "\n")

    @property
    def df(self) -> pd.DataFrame:
        return pd.read_csv(self.csv_path)

    def __len__(self) -> int:
        return len(self.df)


@dataclass(frozen=True)
class ImageDataRowItem:
    url: str
    file_path: str
    label: str
    img_w: str
    img_h: str
    mode: str
    hash_str: str
    format_str: str


class ImagesDataCSV(BaseCSV):
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
        super(ImagesDataCSV, self).__init__(csv_path=csv_path)

    @classmethod
    def create_df_dropped_hash_duplicates(cls, csv_path: Path) -> pd.DataFrame:
        df = pd.read_csv(csv_path)
        df = df.drop_duplicates(subset=[cls.HASH_COL], keep="first")
        return df

    @classmethod
    def split_train_val_test(
            cls,
            df: pd.DataFrame,
            ratio: Tuple[float, float, float]) -> Tuple[pd.DataFrame,
                                                        pd.DataFrame,
                                                        pd.DataFrame]:
        train_ratio, val_ratio, test_ratio = ratio
        df = df[[cls.FILE_PATH_COL, cls.LABEL_COL]]
        labels = df[cls.LABEL_COL]
        train_val_df, test_df, _, _ = train_test_split(
            df, labels, test_size=test_ratio, random_state=0, stratify=labels
        )
        train_val_labels = train_val_df[cls.LABEL_COL]
        test_size = val_ratio / (train_ratio + val_ratio)
        train_df, val_df, _, _ = train_test_split(
            train_val_df, train_val_labels,
            test_size=test_size, random_state=0, stratify=train_val_labels
        )
        return train_df, val_df, test_df


class ImageUrlCSV(BaseCSV):
    URL_COL: str = "url"
    LABEL_COL: str = "label"
    HEADER: List[str] = [URL_COL, LABEL_COL]

    def __init__(self, csv_path: Path):
        super(ImageUrlCSV, self).__init__(csv_path=csv_path)

    def get_row_data_geenrator(self) -> Generator[Tuple[str, str], None, None]:
        df = pd.read_csv(self.csv_path)
        for row in df.itertuples():
            url = getattr(row, self.URL_COL)
            label = getattr(row, self.LABEL_COL)
            yield url, label
