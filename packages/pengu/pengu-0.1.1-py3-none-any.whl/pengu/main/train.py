import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, Any

import tensorflow as tf

from pengu.dataset.image import ImageTFRecord
from pengu.utils.file_io import YamlConfig, load_yaml
from pengu.mlflow import MlflowConfig, MlflowWriter, MlflowCallback
from pengu.model.utils import ModelConfig, build_imagenet_model
from pengu.model.train_utils import prepare_tfds, build_preprocess, build_augment, build_optimizer


AUTOTUNE = tf.data.experimental.AUTOTUNE


@dataclass
class MlflowPreprocessedArtifactsConfig(YamlConfig):
    run_id: str
    train_path: Path
    val_path: Path
    test_path: Path
    label2index_path: Path


@dataclass
class PreprocessConfig(YamlConfig):
    rescale_scale: str  # eval(resize_scale). Exaple: "1./127.5"
    rescale_offset: float
    img_size: Tuple[int, int]


@dataclass
class OptimizerConfig(YamlConfig):
    name: str
    params: Dict[str, Any]


@dataclass
class TrainConfig(YamlConfig):
    input_preprocessed_data: MlflowPreprocessedArtifactsConfig
    preprocess: PreprocessConfig
    augment: Dict[str, dict]  # tf.keras.layers.experimental.preprocessing.{key}(**values)
    model: ModelConfig
    optimizer: OptimizerConfig


@dataclass
class TrainMainConfig(YamlConfig):
    train: TrainConfig
    mlflow: MlflowConfig


def main():
    parser = argparse.ArgumentParser(
        description="Train Keras Model")
    parser.add_argument("--config_path", "-config",
                        type=Path, metavar="path", required=True,
                        help="Config(.yml) file path")
    parser.add_argument("--input_preprocessed_dir", "-i", type=Path, metavar="Path",
                        required=True,
                        help="Path to save preprocessed data")
    parser.add_argument("--output_model_path", "-m", type=Path, metavar="Path",
                        required=True,
                        help="Path to save model")
    parser.add_argument("--tb_logs_path", "-t", type=Path, metavar="Path",
                        required=True,
                        help="Path to write logs for tensorboard")
    parser.add_argument("--batch_size", "-bt", type=int, metavar="train", default=32,
                        help="Batch size")
    parser.add_argument("--epochs", "-e", type=int, metavar="train", default=3,
                        help="epoch")
    args = parser.parse_args()

    config: TrainMainConfig = TrainMainConfig.load(args.config_path)
    train_config: TrainConfig = config.train
    mlflow_config: MlflowConfig = config.mlflow

    # MlflowWriter
    writer = MlflowWriter(experiment_name=mlflow_config.experiment_name,
                          tracking_uri=mlflow_config.tracking_uri,
                          registry_uri=mlflow_config.registry_uri)
    writer.log_params_from_config(train_config)
    # download artifacts from Mlflow
    input_config = train_config.input_preprocessed_data
    train_tfrecord_path = writer.download_artifacts(
        run_id=input_config.run_id,
        path=str(input_config.train_path),
        dst_path=args.input_preprocessed_dir
    )
    val_tfrecord_path = writer.download_artifacts(
        run_id=input_config.run_id,
        path=str(input_config.val_path),
        dst_path=args.input_preprocessed_dir
    )
    test_tfrecord_path = writer.download_artifacts(
        run_id=input_config.run_id,
        path=str(input_config.test_path),
        dst_path=args.input_preprocessed_dir
    )
    label2index_path = writer.download_artifacts(
        run_id=input_config.run_id,
        path=str(input_config.label2index_path),
        dst_path=args.input_preprocessed_dir
    )
    train_ds = ImageTFRecord.read_tfrecord(train_tfrecord_path)
    val_ds = ImageTFRecord.read_tfrecord(val_tfrecord_path)
    test_ds = ImageTFRecord.read_tfrecord(test_tfrecord_path)
    label2index: Dict[str, int] = load_yaml(label2index_path)

    # build preprocess
    preprocess_config = train_config.preprocess
    preprocess = build_preprocess(rescale_scale=preprocess_config.rescale_scale,
                                  rescale_offset=preprocess_config.rescale_offset,
                                  img_size=preprocess_config.img_size)
    # build augment
    augment_config = train_config.augment
    augment = build_augment(augment_config)
    # prepare tf.data.Dataset
    train_ds = prepare_tfds(
        ds=train_ds,
        batch_size=args.batch_size,
        shuffle=True,
        preprocess=preprocess,
        augment=augment
    )
    val_ds = prepare_tfds(
        ds=val_ds,
        batch_size=args.batch_size,
        shuffle=True,
        preprocess=preprocess,
        augment=augment
    )
    test_ds = prepare_tfds(
        ds=test_ds,
        batch_size=args.batch_size,
        shuffle=True,
        preprocess=preprocess,
        augment=augment
    )
    # build_optimizer
    optimizer_config = train_config.optimizer
    optimizer = build_optimizer(optimizer_config.name, optimizer_config.params)
    # build keras model
    model_config = train_config.model
    model_params = model_config.params if model_config.params is not None else {}
    img_shape = preprocess_config.img_size + (3,)
    base_model = build_imagenet_model(
        model_config.name,
        input_shape=img_shape,
        include_top=False,
        **model_params)
    base_model.trainable = False
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(len(label2index))
    ])
    model.compile(optimizer=optimizer,
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    # build callbacks
    args.output_model_path.parent.mkdir(parents=True, exist_ok=True)
    args.tb_logs_path.mkdir(parents=True, exist_ok=True)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=3),
        tf.keras.callbacks.ModelCheckpoint(args.output_model_path),
        tf.keras.callbacks.TensorBoard(args.tb_logs_path),
        MlflowCallback(writer=writer)
    ]
    # train model
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks
    )

    # evaluate model
    loss, accuracy = model.evaluate(test_ds)
    writer.log_metric(key="test_loss", value=loss)
    writer.log_metric(key="test_acc", value=accuracy)
    print("loss: {:.2f}".format(loss))
    print("accuracy: {:.2f}".format(accuracy))

    # add artifacts
    writer.log_artifacts(args.output_model_path)
    writer.set_terminated()


if __name__ == "__main__":
    main()
