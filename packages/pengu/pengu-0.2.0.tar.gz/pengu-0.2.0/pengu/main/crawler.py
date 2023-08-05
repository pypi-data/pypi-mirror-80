import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List

from icrawler.builtin import GoogleImageCrawler

from pengu.crawler import FixedGoogleParser, SaveUrlNotDownloadDownloader
from pengu.core.csv_core import ImageUrlCSV
from pengu.utils.file_io import YamlConfig


@dataclass
class CrawlerMainConfig(YamlConfig):
    keywords: List[str]
    labels: List[str]
    start_date: List[int]  # [2020, 1, 1]
    end_date: List[int]
    max_num: int


def main():
    # parse args
    parser = argparse.ArgumentParser(description="crawling images from google image search")
    parser.add_argument("--output_result_csv", "-csv", type=Path, metavar="Path",
                        required=True,
                        help="Path to result path")
    parser.add_argument("--config_path", "-config",
                        type=Path, metavar="path", default=Path("./params.yaml"),
                        help="Config(.yml) file path")
    parser.add_argument("--feeder_threads", "-f_t", type=int, metavar="crawler", default=1,
                        help="thread number used by feeder")
    parser.add_argument("--parser_threads", "-p_t", type=int, metavar="crawler", default=4,
                        help="thread number used by parser")
    parser.add_argument("--downloader_threads", "-d_t", type=int, metavar="crawler", default=5,
                        help="thread number used by downloader")
    args = parser.parse_args()

    config: CrawlerMainConfig = CrawlerMainConfig.load(args.config_path, process_name="crawler")

    # write header
    if not args.output_result_csv.is_file():
        ImageUrlCSV.write_header(args.output_result_csv)

    filters = dict(
        size="large",
        license="commercial,modify",
        date=(tuple(config.start_date), tuple(config.end_date))
    )

    for keyword, label in zip(config.keywords, config.labels):
        crawler = GoogleImageCrawler(
            feeder_threads=args.feeder_threads,
            parser_threads=args.parser_threads,
            downloader_threads=args.downloader_threads,
            downloader_cls=SaveUrlNotDownloadDownloader,
            parser_cls=FixedGoogleParser,
            extra_downloader_args={"csv_path": args.output_result_csv,
                                   "label": label}
        )
        crawler.crawl(keyword=keyword, filters=filters, max_num=config.max_num)


if __name__ == "__main__":
    main()
