from typing import Optional

import tensorflow as tf

AUTOTUNE = tf.data.experimental.AUTOTUNE


def build(ds: tf.data.Dataset,
          batch_size: int,
          shuffle: bool = False,
          preprocess_fn: Optional[tf.keras.Sequential] = None,
          augment_fn: Optional[tf.keras.Sequential] = None) -> tf.data.Dataset:
    if preprocess_fn is not None:
        ds = ds.map(lambda x, y: (preprocess_fn(x), y),
                    num_parallel_calls=AUTOTUNE)

    ds = ds.cache()
    if shuffle:
        ds = ds.shuffle(batch_size * 8)

    ds = ds.batch(batch_size)

    if augment_fn is not None:
        ds = ds.map(lambda x, y: (augment_fn(x, training=True), y),
                    num_parallel_calls=AUTOTUNE)
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds
