import argparse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple, Optional, Dict

from pengu.crawler import ImagesDataCSV
from pengu.utils.file_io import YamlConfig, save_yaml
from pengu.mlflow import MlflowArtifactsConfig, MlflowConfig, MlflowWriter
from pengu.dataset.image import ImageTFRecord


@dataclass
class PreprocessImagesConfig(YamlConfig):
    input_data_csv: MlflowArtifactsConfig
    input_images: MlflowArtifactsConfig
    ratio: List[float]
    img_size: Tuple[int, int] = (500, 500)
    label2index: Optional[Dict[str, int]] = None


@dataclass
class ProprocessImagesMainConfig(YamlConfig):
    preprocess: PreprocessImagesConfig
    mlflow: MlflowConfig


def main():
    parser = argparse.ArgumentParser(
        description="Remove images with duplicate hash and "
                    "Split dataframe to train and val, test dataframe")
    parser.add_argument("--config_path", "-config",
                        type=Path, metavar="path", required=True,
                        help="Config(.yml) file path")
    parser.add_argument("--output_preprocessed_csv_dir", "-csv", type=Path, metavar="Path",
                        required=True,
                        help="Path to result path")
    args = parser.parse_args()

    config: ProprocessImagesMainConfig = ProprocessImagesMainConfig.load(args.config_path)
    preprocess_config: PreprocessImagesConfig = config.preprocess
    mlflow_config: MlflowConfig = config.mlflow

    # MlflowWriter
    writer = MlflowWriter(experiment_name=mlflow_config.experiment_name,
                          tracking_uri=mlflow_config.tracking_uri,
                          registry_uri=mlflow_config.registry_uri)
    writer.log_params_from_config(preprocess_config)
    # download artifacts from Mlflow
    input_csv_config: MlflowArtifactsConfig = preprocess_config.input_data_csv
    image_data_csv_path = writer.download_artifacts(
        run_id=input_csv_config.run_id,
        path=input_csv_config.path,
        dst_path=args.output_preprocessed_csv_dir
    )
    input_images_config: MlflowArtifactsConfig = preprocess_config.input_images
    images_path = writer.download_artifacts(
        run_id=input_images_config.run_id,
        path=input_images_config.path,
        dst_path=args.output_preprocessed_csv_dir
    )

    # preprocess image data csv
    image_data_csv = ImagesDataCSV(image_data_csv_path)
    image_data_csv.drop_duplicates_hash()
    ratio: Tuple[float, float, float] = tuple(preprocess_config.ratio)
    train_df, val_df, test_df = image_data_csv.split_train_val_test(
        ratio=ratio)
    train_csv_path = args.output_preprocessed_csv_dir / "train.csv"
    val_csv_path = args.output_preprocessed_csv_dir / "val.csv"
    test_csv_path = args.output_preprocessed_csv_dir / "test.csv"
    train_df.to_csv(train_csv_path, index=False)
    val_df.to_csv(val_csv_path, index=False)
    test_df.to_csv(test_csv_path, index=False)

    # make tf.data.Dataset
    train_tfrec_path = args.output_preprocessed_csv_dir / "train.tfrec"
    val_tfrec_path = args.output_preprocessed_csv_dir / "val.tfrec"
    test_tfrec_path = args.output_preprocessed_csv_dir / "test.tfrec"
    if preprocess_config.label2index is None:
        label2index = None
    else:
        label2index = asdict(preprocess_config.label2index)
    label2index_path = args.output_preprocessed_csv_dir / "label2index.yaml"
    train_label2index: Dict[str, int] = ImageTFRecord.write_tfrecord(
        df=train_df,
        img_dst_path=images_path,
        tfrecord_path=train_tfrec_path,
        label2index=label2index,
        img_size=preprocess_config.img_size)
    ImageTFRecord.write_tfrecord(df=val_df,
                                 img_dst_path=images_path,
                                 tfrecord_path=val_tfrec_path,
                                 label2index=train_label2index,
                                 img_size=preprocess_config.img_size)
    ImageTFRecord.write_tfrecord(df=test_df,
                                 img_dst_path=images_path,
                                 tfrecord_path=test_tfrec_path,
                                 label2index=train_label2index,
                                 img_size=preprocess_config.img_size)
    save_yaml(train_label2index, label2index_path)

    # add artifacts
    writer.log_artifact(train_csv_path)
    writer.log_artifact(val_csv_path)
    writer.log_artifact(test_csv_path)
    writer.log_artifact(label2index_path)
    writer.log_artifact(train_tfrec_path)
    writer.log_artifact(val_tfrec_path)
    writer.log_artifact(test_tfrec_path)
    writer.set_terminated()


if __name__ == "__main__":
    main()
