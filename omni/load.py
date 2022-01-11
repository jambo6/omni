"""Basic loading functions."""
import pickle
import json
from pathlib import Path
from typing import Union, Any, Callable
from enum import Enum


class Extension(Enum):
    TEXT = "txt"
    JSON = "json"
    JSONL = "jsonl"
    PICKLE = "pkl"


def load_text_file(path: Union[str, Path]) -> str:
    """Loads a text file."""
    with open(path, "r") as f:
        return f.read()


def save_text_file(text: str, output_path: Union[str, Path]) -> None:
    """Saves a text file."""
    with open(output_path, "w") as f:
        f.write(text)


def load_json(path: Union[str, Path]) -> dict[Any, Any]:
    """Load a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def save_json(json_data: dict[Any, Any], output_path: Union[str, Path]) -> None:
    """Save a JSON file."""
    with open(output_path, "w") as f:
        json.dump(json_data, f)


def load_jsonl(path: Union[str, Path]) -> list[dict[Any, Any]]:
    """Load a JSONL file."""
    with open(path, "r") as f:
        return [json.loads(line) for line in f]


def save_jsonl(jsonl_data: list[dict[Any, Any]], output_path: Union[str, Path]) -> None:
    """Save a JSONL file."""
    with open(output_path, "w") as f:
        for line in jsonl_data:
            f.write(json.dumps(line) + "\n")


def load_pickle(path: Union[str, Path]) -> Any:
    """Loads a pickle file."""
    with open(path, "rb") as f:
        return pickle.load(f)


def save_pickle(data: Any, path: Union[str, Path]) -> None:
    """Saves a pickle file."""
    with open(path, "wb") as f:
        pickle.dump(data, f)


def _reference_dict() -> dict[str, dict[str, Callable]]:
    return {
        "TEXT": {"load": load_text_file, "save": save_text_file},
        "JSON": {"load": load_json, "save": save_json},
        "JSONL": {"load": load_jsonl, "save": save_jsonl},
        "PICKLE": {"load": load_pickle, "save": save_pickle},
    }


def _get_extension(path: Union[str, Path]) -> Extension:
    """Get the enum extension of the path."""
    extension_str = str(path).split(".")[-1]
    allowed_extensions = [x.value for x in Extension]
    if extension_str not in allowed_extensions:
        raise ValueError(f"Extension {extension_str} not found, choose from {allowed_extensions}.")
    return Extension(extension_str)


def load_master(path: Union[str, Path]) -> Any:
    """Master load function that reads the file extension and behaves appropriately."""
    extension = _get_extension(path)
    load_function = _reference_dict()[extension.name]["load"]
    return load_function(path)


def save_master(data: Any, path: Union[str, Path]) -> None:
    """Master save function that reads the file extension and behaves appropriately."""
    extension = _get_extension(path)
    save_function = _reference_dict()[extension.name]["save"]
    return save_function(data, path)
