import argparse
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List

from pengu.core.csv_core import ImageUrlCSV, ImagesDataCSV
from pengu.data.image_download import ImageDownloader
from pengu.utils.file_io import YamlConfig
from pengu.utils.function import set_logging_basic_config


@dataclass
class DownloadMainConfig(YamlConfig):
    resize_max_size: List[int]  # [img_w, img_h]


def main():
    # parse args
    parser = argparse.ArgumentParser(description="downloading images from url csv")
    parser.add_argument("--input_url_csv", "-url_csv", type=Path, metavar="Path",
                        required=True,
                        help="Path to url csv path")
    parser.add_argument("--output_img_data_csv", "-img_csv", type=Path, metavar="Path",
                        required=True,
                        help="Path to image data csv path")
    parser.add_argument("--output_img_dir", "-img_dir", type=Path, metavar="Path",
                        required=True,
                        help="Path to directory to save image")
    parser.add_argument("--n_workers", "-n", type=int, metavar="download",
                        default=10,
                        help="thread number used by downloader")
    parser.add_argument("--retry_count", "-r_c", type=int, metavar="download",
                        default=1,
                        help="Total number of retries to allow")
    parser.add_argument("--retry_backoff_factor", "-r_f", type=float, metavar="download",
                        default=0.1,
                        help="A backoff factor to apply between attempts after the second try")
    parser.add_argument("--timeout", "-t", type=float, metavar="download",
                        default=1.0,
                        help="A timeout to download image")
    parser.add_argument("--config_path", "-config",
                        type=Path, metavar="path", default=Path("./params.yaml"),
                        help="Config(.yml) file path")
    args = parser.parse_args()

    set_logging_basic_config(log_level="INFO")

    config: DownloadMainConfig = DownloadMainConfig.load(args.config_path, process_name="download")

    url_csv = ImageUrlCSV(args.input_url_csv)
    ImagesDataCSV.write_header(args.output_img_data_csv)
    img_data_csv = ImagesDataCSV(args.output_img_data_csv)

    downloader = ImageDownloader(
        n_workers=args.n_workers,
        retry_count=args.retry_count,
        retry_backoff_factor=args.retry_backoff_factor,
        timeout=args.timeout,
        resize_max_size=tuple(config.resize_max_size)  # type: ignore
    )
    logging.info("Start downloading")
    downloader.download(url_csv=url_csv, img_dir=args.output_img_dir, img_data_csv=img_data_csv)
    logging.info("End downloading")


if __name__ == "__main__":
    main()
