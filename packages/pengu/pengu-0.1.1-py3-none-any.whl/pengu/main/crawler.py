import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List

from icrawler.builtin import GoogleImageCrawler

from pengu.crawler import ImagesDataCSV, SaveResultImageDownloader, FixedGoogleParser
from pengu.utils.file_io import YamlConfig
from pengu.mlflow import MlflowWriter, MlflowConfig


@dataclass
class CrawlerConfig(YamlConfig):
    keywords: List[str]
    labels: List[str]
    start_date: List[int]  # [2020, 1, 1]
    end_date: List[int]


@dataclass
class CrawlerMainConfig(YamlConfig):
    crawler: CrawlerConfig
    mlflow: MlflowConfig


def main():
    # parse args
    parser = argparse.ArgumentParser(description="crawling images from google image search")
    parser.add_argument("--config_path", "-config",
                        type=Path, metavar="path", required=True,
                        help="Config(.yml) file path")
    parser.add_argument("--output_result_csv", "-csv", type=Path, metavar="Path",
                        required=True,
                        help="Path to result path")
    parser.add_argument("--output_images_root_dir", "-i", type=Path, metavar="Path",
                        required=True,
                        help="Path to the root directory for images to save")
    parser.add_argument("--max_num", "-n", type=int, metavar="crawler",
                        required=True,
                        help="Downloaded image number has reached required number")
    parser.add_argument("--feeder_threads", "-f_t", type=int, metavar="crawler", default=1,
                        help="thread number used by feeder")
    parser.add_argument("--parser_threads", "-p_t", type=int, metavar="crawler", default=4,
                        help="thread number used by parser")
    parser.add_argument("--downloader_threads", "-d_t", type=int, metavar="crawler", default=5,
                        help="thread number used by downloader")
    args = parser.parse_args()

    config: CrawlerMainConfig = CrawlerMainConfig.load(args.config_path)
    crawler_config: CrawlerConfig = config.crawler
    mlflow_config: MlflowConfig = config.mlflow

    # MlflowWriter
    writer = MlflowWriter(experiment_name=mlflow_config.experiment_name,
                          tracking_uri=mlflow_config.tracking_uri,
                          registry_uri=mlflow_config.registry_uri)
    writer.log_params_from_config(crawler_config)

    # write header
    if not args.output_result_csv.is_file():
        ImagesDataCSV.write_header(args.output_result_csv)

    filters = dict(
        size="large",
        license="commercial,modify",
        date=(tuple(crawler_config.start_date), tuple(crawler_config.end_date))
    )

    for keyword, label in zip(crawler_config.keywords, crawler_config.labels):
        images_root_dir = args.output_images_root_dir / keyword.replace(" ", "_")
        crawler = GoogleImageCrawler(
            feeder_threads=args.feeder_threads,
            parser_threads=args.parser_threads,
            downloader_threads=args.downloader_threads,
            storage={"root_dir": images_root_dir},
            downloader_cls=SaveResultImageDownloader,
            parser_cls=FixedGoogleParser,
            extra_downloader_args={"image_data_csv_path": args.output_result_csv,
                                   "label": label}
        )
        crawler.crawl(keyword=keyword, filters=filters, max_num=args.max_num)

    # add artifacts
    writer.log_artifact(args.output_result_csv)
    writer.log_artifacts(args.output_images_root_dir)
    writer.set_terminated()


if __name__ == "__main__":
    main()
