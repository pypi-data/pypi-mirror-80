from typing import Dict, Any

import tensorflow as tf


def build(config: Dict[str, Any]) -> tf.keras.Sequential:
    """Builds augment step based on the configuration.

    Args:
        config (Dict[str, Any]): tf.keras.layers.experimental.preprocessing.{key}(**values)

    Returns:
        tf.keras.Sequential: A callable function and an argument map to call function with.
    """
    augment_list = []
    for key, kwargs in config.items():
        augment_class = getattr(tf.keras.layers.experimental.preprocessing, key)
        augment_list.append(augment_class(**kwargs))
    return tf.keras.Sequential(augment_list)
