from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Any, Optional

import tensorflow as tf
from mlflow.tracking.client import MlflowClient

from pengu.utils.file_io import YamlConfig


@dataclass
class MlflowArtifactsConfig(YamlConfig):
    run_id: str
    path: str


@dataclass
class MlflowConfig(YamlConfig):
    experiment_name: str
    tracking_uri: Optional[str] = "http://localhost:5000"
    registry_uri: Optional[str] = None


class MlflowWriter(object):
    def __init__(self,
                 experiment_name: str,
                 tracking_uri: Optional[str] = None,
                 registry_uri: Optional[str] = None):
        self.client = MlflowClient(tracking_uri=tracking_uri, registry_uri=registry_uri)
        try:
            self.experiment_id = self.client.create_experiment(experiment_name)
        except Exception:
            self.experiment_id = self.client.get_experiment_by_name(experiment_name).experiment_id

        self.run_id = self.client.create_run(self.experiment_id).info.run_id

    def log_params_from_config(self, config: object):
        params = asdict(config)
        for key, value in params.items():
            self._log_param_recursive(key, value)

    def _log_param_recursive(self, parent_key, parent_value):
        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                if isinstance(value, (dict, list, tuple)):
                    self._log_param_recursive(f'{parent_key}.{key}', value)
                else:
                    self.client.log_param(self.run_id, f'{parent_key}.{key}', str(value))
        else:
            self.client.log_param(self.run_id, f'{parent_key}', str(parent_value))

    def log_param(self, key: str, value: Any):
        self.client.log_param(self.run_id, key, str(value))

    def log_metric(self, key: str, value: Any, step: Optional[int] = None):
        self.client.log_metric(self.run_id, key, value, step=step)

    def log_artifact(self, path: Path):
        self.client.log_artifact(self.run_id, str(path))

    def log_artifacts(self, path: Path):
        self.client.log_artifact(self.run_id, str(path))

    def set_terminated(self):
        self.client.set_terminated(self.run_id)

    def download_artifacts(self,
                           run_id: str,
                           path: str,
                           dst_path: Path) -> Path:
        dst_path.mkdir(parents=True, exist_ok=True)
        artifacts_path = self.client.download_artifacts(run_id=run_id,
                                                        path=path,
                                                        dst_path=str(dst_path))
        return Path(artifacts_path)


class MlflowCallback(tf.keras.callbacks.Callback):
    def __init__(self, writer: MlflowWriter):
        self.writer = writer

    def on_epoch_end(self, epoch, logs):
        for key, value in logs.items():
            self.writer.log_metric(key=key, value=value, step=epoch)
