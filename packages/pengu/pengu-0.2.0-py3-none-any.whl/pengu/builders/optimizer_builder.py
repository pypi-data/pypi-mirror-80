from dataclasses import dataclass
from typing import Dict, Any, Optional

import tensorflow as tf

from pengu.utils.file_io import YamlConfig


@dataclass
class OptimizerConfig(YamlConfig):
    name: str
    params: Optional[Dict[str, Any]] = None


def build(config: OptimizerConfig) -> tf.keras.optimizers.Optimizer:
    opt_class = getattr(tf.keras.optimizers, config.name)
    params = config.params if config.params is not None else {}
    return opt_class(**params)
