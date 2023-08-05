import re
import time
import logging
import absl.logging
from datetime import datetime
from typing import Any, List

from pytz import timezone, utc


def alpha_numeric_sorted(values: List[str]) -> List[str]:
    """Sort the given iterable in the way that humans expect.
    Args:
        l (List[str]): list will be sorted.
    Returns:
        List[str]: list sorted by alpha numeric method.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(values, key=alphanum_key)


def customTime(*args: Any) -> time.struct_time:
    """Convert timezone to "Asia/Tokyo" for logging.
    Returns:
        time.struct_time: Converter timezone to "Asia/Tokyo"
    """
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("Asia/Tokyo")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()


def set_logging_basic_config(log_level: str = "INFO") -> None:
    """Build logging logger
    Args:
        log_level (str): log_level.
                         Defaults to "INFO".
    """
    # NOTE: https://github.com/tensorflow/tensorflow/issues/27045
    logging.root.removeHandler(absl.logging._absl_handler)
    absl.logging._warn_preinit_stderr = False

    logging.Formatter.converter = customTime
    log_fmt = logging.Formatter('%(asctime)s %(name)s %(lineno)d '
                                '[%(levelname)s][%(funcName)s] %(message)s')
    s_handler = logging.StreamHandler()
    s_handler.setLevel(log_level)
    s_handler.setFormatter(log_fmt)
    logging.basicConfig(handlers=[s_handler], level=log_level)
