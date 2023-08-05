from typing import Optional, Tuple, Dict, Any

import tensorflow as tf

AUTOTUNE = tf.data.experimental.AUTOTUNE


def prepare_tfds(ds: tf.data.Dataset,
                 batch_size: int,
                 shuffle: bool = False,
                 preprocess: Optional[tf.keras.Sequential] = None,
                 augment: Optional[tf.keras.Sequential] = None) -> tf.data.Dataset:
    if preprocess is not None:
        ds = ds.map(lambda x, y: (preprocess(x), y),
                    num_parallel_calls=AUTOTUNE)

    ds = ds.cache()
    if shuffle:
        ds = ds.shuffle(batch_size * 8)

    ds = ds.batch(batch_size)

    if augment is not None:
        ds = ds.map(lambda x, y: (augment(x, training=True), y),
                    num_parallel_calls=AUTOTUNE)
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds


def build_preprocess(rescale_scale: str,
                     rescale_offset: float,
                     img_size: Optional[Tuple[int, int]]) -> tf.keras.Sequential:
    preprocess_list = []
    if img_size is not None:
        preprocess_list.append(
            tf.keras.layers.experimental.preprocessing.Resizing(img_size[0], img_size[1])
        )

    rescale_scale_float = eval(rescale_scale)
    preprocess_list.append(
        tf.keras.layers.experimental.preprocessing.Rescaling(
            rescale_scale_float, offset=rescale_offset)
    )
    return tf.keras.Sequential(preprocess_list)


def build_augment(augment_params: Dict[str, Any]) -> tf.keras.Sequential:
    augment_list = []
    for key, kwargs in augment_params.items():
        augment_class = getattr(tf.keras.layers.experimental.preprocessing, key)
        augment_list.append(augment_class(**kwargs))
    return tf.keras.Sequential(augment_list)


def build_optimizer(name: str, params: Dict[str, Any] = {}) -> tf.keras.optimizers.Optimizer:
    opt_class = getattr(tf.keras.optimizers, name)
    return opt_class(**params)
