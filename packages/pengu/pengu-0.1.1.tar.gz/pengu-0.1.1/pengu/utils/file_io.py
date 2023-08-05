import json
import inspect
import pickle
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional

import yaml


def save_pkl(data: Any, path: Path) -> None:
    """Save data to pickle file path

    Args:
        data (Any): Object to save
        path (Path): pickle file path to save

    """
    with open(path, mode='wb') as f:
        pickle.dump(data, f)


def load_pkl(path: Path) -> Any:
    """Load pickle file path

    Args:
        path (Path): pickle file path to load

    Returns:
        Any: Object that loaded the pickle file path

    """
    with open(path, mode='rb') as f:
        out = pickle.load(f)
    return out


def save_json(data: Any, path: Path) -> None:
    """Save data to json file path

    Args:
        data (Any): Data to save
        path (Path): Json file path to load

    """
    with open(path, 'w') as f:
        json.dump(data, f)


def load_json(path: Path) -> dict:
    """Load json file path

    Args:
        path (Path): Json file path to load

    Returns:
        dict: Data read from json file

    """
    with open(path) as f:
        json_dict = json.load(f)
    return json_dict


def save_yaml(data: Any, path: Path) -> None:
    """Save data to yaml file path

    Args:
        data (Any): Data to save
        path (Path): Yaml file path to save

    """
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def load_yaml(path: Path) -> dict:
    """Load yaml file path

    Args:
        path (Path): Yaml file path to load

    Returns:
        dict: Data read from yaml file

    """
    with open(path) as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
    return yaml_dict


@dataclass
class YamlConfig:
    def save(self, config_path: Path):
        """Export config as YAML file """
        config_path.parent.mkdir(exist_ok=True)

        def convert_dict_for_pathlib(data):
            for key, val in data.items():
                if isinstance(val, Path):
                    data[key] = str(val)
                if isinstance(val, dict):
                    data[key] = convert_dict_for_pathlib(val)
            return data

        with open(config_path, 'w') as f:
            yaml.dump(convert_dict_for_pathlib(asdict(self)), f)

    @classmethod
    def load(cls, config_path: Path):
        """Load config from YAML file """

        def convert_from_dict(parent_cls, data):
            for key, val in data.items():
                child_class = parent_cls.__dataclass_fields__[key].type
                if child_class == Optional[Path] and val is not None:
                    data[key] = Path(val)
                if child_class == Path:
                    data[key] = Path(val)
                if hasattr(child_class, "_name"):
                    if child_class._name == "Tuple":
                        data[key] = tuple(val)
                if inspect.isclass(child_class) and issubclass(child_class, YamlConfig):
                    data[key] = child_class(**convert_from_dict(child_class, val))
            return data

        with open(config_path) as f:
            config_data = yaml.full_load(f)
            # recursively convert config item to YamlConfig
            config_data = convert_from_dict(cls, config_data)

        return cls(**config_data)  # type: ignore
