from dataclasses import dataclass
from typing import List

import tensorflow as tf

from pengu.utils.file_io import YamlConfig


@dataclass
class PreprocessConfig(YamlConfig):
    rescale_scale: str  # eval(resize_scale). Exaple: "1./127.5"
    rescale_offset: float
    img_size: List[int]  # (img_w, img_h)


def build(config: PreprocessConfig) -> tf.keras.Sequential:
    img_w, img_h = config.img_size
    rescale_scale_float = eval(config.rescale_scale)
    preprocess_fn = tf.keras.Sequential([
        tf.keras.layers.experimental.preprocessing.Resizing(img_h, img_w),
        tf.keras.layers.experimental.preprocessing.Rescaling(
            rescale_scale_float, offset=config.rescale_offset)
    ])

    return preprocess_fn
