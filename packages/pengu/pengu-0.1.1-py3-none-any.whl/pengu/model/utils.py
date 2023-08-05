from dataclasses import dataclass
from typing import Optional, Tuple, Any, Dict

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
class ModelConfig(YamlConfig):
    name: str
    params: Optional[Dict[str, Any]] = None


def build_imagenet_model(model_name: str,
                         **kwargs) -> tf.keras.Model:
    """build keras application models and Return input shape.

    Args:
        model_name (str):
            Name of model supported by keras.applications.

    Returns:
        keras.engine.training.Model: built model.

    """
    model_name = model_name.lower()
    input_shape = kwargs.pop("input_shape", get_imagenet_input_shape(model_name))

    if model_name == 'xception':
        model = Xception(input_shape=input_shape, **kwargs)
    elif model_name == 'vgg16':
        model = VGG16(input_shape=input_shape, **kwargs)
    elif model_name == 'vgg19':
        model = VGG19(input_shape=input_shape, **kwargs)
    elif model_name == 'resnet50':
        model = ResNet50(input_shape=input_shape, **kwargs)
    elif model_name in ['inception_v3', 'inceptionv3']:
        model = InceptionV3(input_shape=input_shape, **kwargs)
    elif model_name in ['inception_resnet_v2', 'inceptionresnetv2']:
        model = InceptionResNetV2(input_shape=input_shape, **kwargs)
    elif model_name == 'mobilenet':
        model = MobileNet(input_shape=input_shape, **kwargs)
    elif model_name in ['densenet_201', 'densenet201']:
        model = DenseNet201(input_shape=input_shape, **kwargs)
    elif model_name in ['nasnet_large', 'nasnetlarge']:
        model = NASNetLarge(input_shape=input_shape, **kwargs)
    elif model_name in ['nasnet_mobile', 'nasnetmobilne']:
        model = NASNetMobile(input_shape=input_shape, **kwargs)
    elif model_name in ['mobilenet_v2', 'mobilenetv2']:
        model = MobileNetV2(input_shape=input_shape, **kwargs)
    else:
        raise NotImplementedError(f"Not implemented. model_name: {model_name}")

    return model


def get_imagenet_input_shape(model_name: str) -> Optional[Tuple[int, int, int]]:
    """Return input shape of keras.applications model.

    Args:
        model_name (str):
            Name of model supported by keras.applications.

    Returns:
        Optional[Tuple[int, int, int]]: (height, width, channels)

    """
    model_name = model_name.lower()

    if model_name == 'xception':
        input_shape: Optional[Tuple[int, int, int]] = (299, 299, 3)
    elif model_name == 'vgg16':
        input_shape = (224, 224, 3)
    elif model_name == 'vgg19':
        input_shape = (224, 224, 3)
    elif model_name == 'resnet50':
        input_shape = (224, 224, 3)
    elif model_name in ['inception_v3', 'inceptionv3']:
        input_shape = (299, 299, 3)
    elif model_name in ['inception_resnet_v2', 'inceptionresnetv2']:
        input_shape = (299, 299, 3)
    elif model_name == 'mobilenet':
        input_shape = (224, 224, 3)
    elif model_name in ['densenet_201', 'densenet201']:
        input_shape = (224, 224, 3)
    elif model_name in ['nasnet_large', 'nasnetlarge']:
        input_shape = (331, 331, 3)
    elif model_name in ['nasnet_mobile', 'nasnetmobilne']:
        input_shape = (224, 224, 3)
    elif model_name in ['mobilenet_v2', 'mobilenetv2']:
        input_shape = (224, 224, 3)
    else:
        input_shape = None

    return input_shape
