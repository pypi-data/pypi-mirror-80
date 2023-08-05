from dataclasses import dataclass
from typing import Callable, Optional, Tuple, List, Dict, Union

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.applications.densenet import DenseNet201
from tensorflow.keras.applications.nasnet import NASNetLarge
from tensorflow.keras.applications.nasnet import NASNetMobile
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2

from pengu.utils.file_io import YamlConfig


@dataclass
class BaseModelConfig(YamlConfig):
    name: str
    input_shape: Optional[Union[List[int], Tuple[int, int, int]]] = None  # [img_h, img_w, channel]
    weights: str = "imagenet"
    trainable: bool = False


@dataclass
class TopModelConfig(YamlConfig):
    dropout_rate: float
    n_classes: Optional[int] = None


@dataclass
class ModelConfig(YamlConfig):
    base_model: BaseModelConfig
    top_model: TopModelConfig


KERAS_APPLICATION_MODEL_INPUT_SHAPE_MAP: Dict[str, Tuple[int, int, int]] = {
    "xception": (299, 299, 3),
    "vgg16": (224, 224, 3),
    "vgg19": (224, 224, 3),
    "resnet50": (224, 224, 3),
    "inceptionv3": (299, 299, 3),
    "inception_v3": (299, 299, 3),
    "inception_resnet_v2": (299, 299, 3),
    "inceptionresnetv2": (299, 299, 3),
    "mobilenet": (224, 224, 3),
    "mobilenet_v2": (224, 224, 3),
    "mobilenetv2": (224, 224, 3),
    "densenet_201": (224, 224, 3),
    "densenet201": (224, 224, 3),
    "nasnet_large": (331, 331, 3),
    "nasnetlarge": (331, 331, 3),
    "nasnet_mobile": (224, 224, 3),
    "nasnetmobilne": (224, 224, 3)
}


KERAS_APPLICATION_MODEL_CLASS_MAP: Dict[str, Callable] = {
    "xception": Xception,
    "vgg16": VGG16,
    "vgg19": VGG19,
    "resnet50": ResNet50,
    "inceptionv3": InceptionV3,
    "inception_v3": InceptionV3,
    "inception_resnet_v2": InceptionResNetV2,
    "inceptionresnetv2": InceptionResNetV2,
    "mobilenet": MobileNet,
    "mobilenet_v2": MobileNetV2,
    "mobilenetv2": MobileNetV2,
    "densenet_201": DenseNet201,
    "densenet201": DenseNet201,
    "nasnet_large": NASNetLarge,
    "nasnetlarge": NASNetLarge,
    "nasnet_mobile": NASNetMobile,
    "nasnetmobilne": NASNetMobile
}


def _build_base_model(config: BaseModelConfig) -> tf.keras.Model:
    model_name = config.name.lower()
    _input_shape = config.input_shape
    if _input_shape is None:
        input_shape = KERAS_APPLICATION_MODEL_INPUT_SHAPE_MAP[model_name]
    else:
        # Tuple[int, int, int]
        input_shape = tuple(_input_shape)  # type: ignore

    if model_name in KERAS_APPLICATION_MODEL_CLASS_MAP:
        model_class = KERAS_APPLICATION_MODEL_CLASS_MAP[model_name]
    else:
        raise NotImplementedError("Only keras application models are supported")

    model = model_class(input_shape=input_shape,
                        include_top=False,
                        weights=config.weights)
    return model


def _build_top_model(config: TopModelConfig) -> tf.keras.Model:
    model = tf.keras.Sequential([
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(config.dropout_rate),
        tf.keras.layers.Dense(config.n_classes)
    ])
    return model


def build(config: ModelConfig) -> tf.keras.Model:
    """build keras application models and Return input shape.

    Args:
        model_name (str):
            Name of model supported by keras.applications.

    Returns:
        keras.engine.training.Model: built model.

    """
    base_model = _build_base_model(config.base_model)
    top_model = _build_top_model(config.top_model)
    model = tf.keras.Sequential([base_model, top_model])

    return model
