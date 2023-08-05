import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import tensorflow as tf

from pengu.dataset.image import ImageTFRecord
from pengu.utils.file_io import YamlConfig, load_yaml
from pengu.builders import dataset_builder
from pengu.builders import preprocessor_builder
from pengu.builders import augmenter_builder
from pengu.builders import optimizer_builder
from pengu.builders import model_builder


@dataclass
class TrainClfMainConfig(YamlConfig):
    preprocess: preprocessor_builder.PreprocessConfig
    augment: Dict[str, dict]  # tf.keras.layers.experimental.preprocessing.{key}(**values)
    optimizer: optimizer_builder.OptimizerConfig
    model: model_builder.ModelConfig


def main():
    parser = argparse.ArgumentParser(description="Train Keras Model")
    parser.add_argument("--input_tfrecord_dir", "-tfrecord", type=Path, metavar="Path",
                        required=True,
                        help="Path to save preprocessed data")
    parser.add_argument("--input_label2index", "-l2i", type=Path, metavar="Path",
                        required=True,
                        help="[input] Path to label2index.yaml")
    parser.add_argument("--output_model_path", "-model", type=Path, metavar="Path",
                        required=True,
                        help="[output] Path to save model")
    parser.add_argument("--tb_logs_path", "-t", type=Path, metavar="Path",
                        required=True,
                        help="Path to write logs for tensorboard")
    parser.add_argument("--batch_size", "-bt", type=int, metavar="train", default=32,
                        help="Batch size")
    parser.add_argument("--epochs", "-e", type=int, metavar="train", default=3,
                        help="epoch")
    parser.add_argument("--config_path", "-config",
                        type=Path, metavar="path", default=Path("./params.yaml"),
                        help="Config(.yml) file path")
    args = parser.parse_args()

    config: TrainClfMainConfig = TrainClfMainConfig.load(args.config_path, process_name="train_clf")
    train_tfrec_path = args.input_tfrecord_dir / "train.tfrec"
    val_tfrec_path = args.input_tfrecord_dir / "val.tfrec"
    test_tfrec_path = args.input_tfrecord_dir / "test.tfrec"
    train_ds = ImageTFRecord.read_tfrecord(train_tfrec_path)
    val_ds = ImageTFRecord.read_tfrecord(val_tfrec_path)
    test_ds = ImageTFRecord.read_tfrecord(test_tfrec_path)
    label2index: Dict[str, int] = load_yaml(args.input_label2index)

    # build preprocess
    preprocess_fn: tf.keras.Sequential = preprocessor_builder.build(
        config=config.preprocess
    )
    # build augment
    augment_fn = augmenter_builder.build(config.augment)
    # prepare tf.data.Dataset
    train_ds = dataset_builder.build(
        ds=train_ds,
        batch_size=args.batch_size,
        shuffle=True,
        preprocess_fn=preprocess_fn,
        augment_fn=augment_fn
    )
    val_ds = dataset_builder.build(
        ds=val_ds,
        batch_size=args.batch_size,
        shuffle=True,
        preprocess_fn=preprocess_fn,
        augment_fn=augment_fn
    )
    test_ds = dataset_builder.build(
        ds=test_ds,
        batch_size=args.batch_size,
        shuffle=True,
        preprocess_fn=preprocess_fn,
        augment_fn=augment_fn
    )
    # build_optimizer
    optimizer = optimizer_builder.build(config.optimizer)
    # build keras model
    model_config: model_builder.ModelConfig = config.model
    img_w, img_h = config.preprocess.img_size
    img_shape = (img_h, img_w, 3)
    model_config.base_model.input_shape = img_shape
    model_config.top_model.n_classes = len(label2index)
    model = model_builder.build(model_config)
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
    print("loss: {:.2f}".format(loss))
    print("accuracy: {:.2f}".format(accuracy))


if __name__ == "__main__":
    main()
