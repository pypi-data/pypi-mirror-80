import io
import functools
from pathlib import Path
from typing import Tuple, Optional, Dict

import pandas as pd
import tensorflow as tf
from PIL import Image

from pengu.crawler import ImagesDataCSV
from pengu.dataset.utils import _int64_feature, _bytes_feature


AUTOTUNE = tf.data.experimental.AUTOTUNE


def load_and_resize_image(path: Path,
                          img_size: Optional[Tuple[int, int]] = None,
                          serialize: bool = False):
    """
    Examples:
        if set img_size, use unctools.partial.
        >>> load_and_resize_from_path_fn \
            = functools.partial(load_and_resize_from_path, img_size=(img_h, img_w))
        >>> ds = ds.map(load_and_resize_from_path_fn)
    """
    img = Image.open(str(path))
    if img.mode != "RGB":
        img = img.convert("RGB")

    if img_size is not None:
        img = img.resize((img_size[1], img_size[0]))
    img = tf.image.decode_image(img, channels=3)
    if img_size is not None:
        img = tf.image.resize(img, img_size)
    if serialize:
        img = tf.io.serialize_tensor(img)
    return img


def make_tf_dataset(
        df: pd.DataFrame,
        img_dst_path: Path,
        img_size: Optional[Tuple[int, int]] = None,
        serialize: bool = True) -> tf.data.Dataset:
    image_paths = df[ImagesDataCSV.FILE_PATH_COL].to_list()
    image_paths = [str(img_dst_path / path) for path in image_paths]
    labels = df[ImagesDataCSV.LABEL_COL].to_list()
    ds = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    load_and_resize_from_path_fn \
        = functools.partial(load_and_resize_image, img_size=img_size, serialize=serialize)
    ds = ds.map(load_and_resize_from_path_fn, num_parallel_calls=AUTOTUNE)
    return ds


class ImageTFRecord(object):
    IMG_KEY: str = "image"
    LABEL_KEY: str = "label"
    HEIGHT_KEY: str = "height"
    WIDTH_KEY: str = "width"
    CHANNELS_KEY: str = "channels"

    @classmethod
    def _serialize_example(cls,
                           path: Path,
                           label: int,
                           img_size: Optional[Tuple[int, int]] = None) -> tf.train.Example:
        img = Image.open(str(path))
        if img.mode != "RGB":
            img = img.convert("RGB")

        if img_size is not None:
            img = img.resize((img_size[1], img_size[0]))

        _img_bytes = io.BytesIO()
        img.save(_img_bytes, format="JPEG")
        img_bytes = _img_bytes.getvalue()

        img_w, img_h = img.size
        img_shape: Tuple[int, int, int] = (img_h, img_w, 3)
        feature = {
            cls.LABEL_KEY: _int64_feature(label),
            cls.IMG_KEY: _bytes_feature(img_bytes),
            cls.HEIGHT_KEY: _int64_feature(img_shape[0]),
            cls.WIDTH_KEY: _int64_feature(img_shape[1]),
            cls.CHANNELS_KEY: _int64_feature(img_shape[2]),
        }
        return tf.train.Example(features=tf.train.Features(feature=feature))

    @classmethod
    def _desrialize_example(cls, serialized_example):
        image_feature_description = {
            cls.LABEL_KEY: tf.io.FixedLenFeature([], tf.int64),
            cls.IMG_KEY: tf.io.FixedLenFeature([], tf.string),
            cls.HEIGHT_KEY: tf.io.FixedLenFeature((), tf.int64),
            cls.WIDTH_KEY: tf.io.FixedLenFeature((), tf.int64),
            cls.CHANNELS_KEY: tf.io.FixedLenFeature((), tf.int64)
        }
        example = tf.io.parse_single_example(serialized_example,
                                             image_feature_description)
        image = tf.io.decode_image(example[cls.IMG_KEY], channels=3)
        image_shape = [example[cls.HEIGHT_KEY], example[cls.WIDTH_KEY], example[cls.CHANNELS_KEY]]
        image = tf.reshape(image, image_shape)
        return image, example[cls.LABEL_KEY]

    @classmethod
    def write_tfrecord(cls,
                       df: pd.DataFrame,
                       img_dst_path: Path,
                       tfrecord_path: Path,
                       label2index: Optional[Dict[str, int]] = None,
                       img_size: Optional[Tuple[int, int]] = None) -> Dict[str, int]:
        image_paths = df[ImagesDataCSV.FILE_PATH_COL].to_list()
        image_paths = [img_dst_path / path for path in image_paths]
        labels = df[ImagesDataCSV.LABEL_COL].to_list()
        if label2index is None:
            _label2index: Dict[str, int] = {label: i for i, label in enumerate(list(set(labels)))}
        else:
            _label2index = label2index

        with tf.io.TFRecordWriter(str(tfrecord_path)) as writer:
            for path, label in zip(image_paths, labels):
                label_i = _label2index[label]
                tf_example = cls._serialize_example(path, label_i, img_size)
                writer.write(tf_example.SerializeToString())
        return _label2index

    @classmethod
    def read_tfrecord(cls, tfrecord_path: Path) -> tf.data.Dataset:
        raw_ds = tf.data.TFRecordDataset(str(tfrecord_path))

        parsed_ds = raw_ds.map(cls._desrialize_example, num_parallel_calls=AUTOTUNE)
        return parsed_ds
