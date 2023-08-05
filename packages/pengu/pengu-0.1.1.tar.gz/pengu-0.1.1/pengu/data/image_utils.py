import os
import io
import glob
from typing import List, Tuple, Optional, Union

import cv2
import numpy as np
import imagehash
import requests
import PIL
from PIL import Image
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from tensorflow.keras.preprocessing import image as keras_image

from pengu.utils.function import alpha_numeric_sorted
from pengu.exceptions import DownloadError


def pil2cv(img: Image.Image) -> np.ndarray:
    """Convert PIL.Image.Image to np.ndarray(opencv)
    Args:
        img (Image.Image): PIL image
    Returns:
        np.ndarray: converted image array (opencv)
    """
    img_np = np.array(img, dtype=np.uint8)
    if img_np.ndim == 2:  # L
        pass
    elif img_np.shape[2] == 3:  # RGB
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    elif img_np.shape[2] == 4:  # RGBA
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA)
    return img_np


def cv2pil(img: np.ndarray) -> Image.Image:
    """Convert np.ndarray(opencv) to PIL.Image.Image
    Args:
        img (np.ndarray): OpenCV image array
    Returns:
        Image.Image: PIL image
    """
    img_np = img.copy()
    if img_np.ndim == 2:  # L
        pass
    elif img_np.shape[2] == 3:  # RGB
        img_np = img_np[:, :, ::-1]
    elif img_np.shape[2] == 4:  # RGBA
        img_np = img_np[:, :, [2, 1, 0, 3]]
    img_pil = Image.fromarray(img_np)
    return img_pil


def download_image(url: str,
                   timeout: float = 1.0,
                   retry_count: int = 3,
                   retry_backoff_factor: float = 0.5) -> Image.Image:
    """Download Image from image url

    Args:
        url (str): image url

    Raises:
        DownloadError

    Returns:
        Image.Image: PIL Image.
    """
    session = requests.Session()

    retries = Retry(total=retry_count,
                    backoff_factor=retry_backoff_factor)

    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(url, timeout=timeout)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise DownloadError(f"Failed to download Image. url: {url}") from e

    try:
        img = Image.open(io.BytesIO(response.content))
    except OSError as e:
        raise DownloadError(f"Failed to open image downloaded. url: {url}") from e

    return img


def load_image(file_path: str,
               target_size: Tuple[int, int]) -> np.ndarray:
    """load image from file path.

    Args:
        file_path_list (List[str]): Image file path list.
        target_size (Tuple[int, int]): Size when load image.

    Returns:
        np.ndarray: Preprocessed and resized image array. Shape is (h, w, ch)

    """
    img = keras_image.load_img(file_path, target_size=target_size)
    img = np.asarray(img)

    return img


def list_pictures(dir_path: str,
                  n_use: int = -1,
                  ext: Tuple[str, ...] = ('jpg', 'jpeg', 'bmp', 'png', 'tif')) -> List[str]:
    """Lists all pictures in a directory, not including all subdirectories.

    Args
        dir_path (str): Absolute path to the directory.
        ext (Tuple[str, ...]): Extensions of the pictures.

    Returns
        A list of paths.

    """
    ext = tuple('.%s' % e for e in ((ext,) if isinstance(ext, str) else ext))

    picture_file_list = [file for file in glob.glob(os.path.join(dir_path, '*'))
                         if file.lower().endswith(ext)]

    picture_file_list = alpha_numeric_sorted(picture_file_list)
    if n_use != -1:
        picture_file_list = picture_file_list[:n_use]

    return picture_file_list


def get_image_meta(data: Union[np.ndarray, Image.Image, str],
                   data_format: str,
                   hash_method: str) -> Tuple[Tuple[int, int],
                                              Optional[str],
                                              Optional[imagehash.ImageHash],
                                              Optional[str]]:
    """Get image meta data(size[w, h], mode, hash)

    Args:
        data (Union[np.ndarray, Image.Image, str]):
            image data. support data_format data.
        data_format (str):
            support "url" and "file"(path), "pil", "opencv".
        hash_method (str):
            support "phash" and "average", "dhash", "whash".

    Returns:
        Tuple[Tuple[int, int], Optional[str], Optional[imagehash.ImageHash]]]:
            (size[w, h], image_mode, hash, img_format).
            if DownloadError, ((0,0), None, None, None).
    """
    if isinstance(data, str):
        if data_format == 'url':
            try:
                img: Image.Image = download_image(data)
            except DownloadError:
                return (0, 0), None, None, None
        elif data_format == 'file':
            img = Image.open(data)
        else:
            raise ValueError(f"Invalid data: {data}, data_format: {data_format}")
    elif type(data).__module__.startswith(PIL.__name__):
        if data_format == 'pil':
            img = data
        else:
            raise ValueError(f"Invalid data. data_format: {data_format}")
    elif type(data).__module__.startswith(np.__name__):
        if data_format == 'opencv':
            img = cv2pil(data)
        else:
            raise ValueError(f"Invalid data. data_format: {data_format}")
    else:
        raise ValueError("Invalid data. data_type: "
                         f"{type(data).__module__}, data_format: {data_format}")

    if hash_method == "phash":
        hash_func = imagehash.phash
    elif hash_method == "average":
        hash_func = imagehash.average_hash
    elif hash_method == "dhash":
        hash_func = imagehash.dhash
    elif hash_method == "whash":
        hash_func = imagehash.whash
    else:
        raise ValueError(f"Invalid hashmethod. hash_method: {hash_method}")

    img_hash = hash_func(img)
    img_format = img.format
    return img.size, img.mode, img_hash, img_format
