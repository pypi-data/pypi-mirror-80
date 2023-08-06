import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Generic, Iterable, Literal, Optional, Type, TypeVar

from pydantic import BaseModel, FilePath
from ruamel.yaml import YAML

from autogram_commons.identifiable import IdentifiableBaseModel, Identity

TEntity = TypeVar("TEntity", bound=IdentifiableBaseModel, covariant=True)
TRoot = TypeVar("TRoot", bound=BaseModel)


class FileDataLoader(Generic[TEntity, TRoot], ABC):
    def __init__(self, file_path: FilePath, root_type: Type[TRoot]):
        self.file_path: Path = file_path
        assert self.file_path.exists()
        self.root_type: Type[TRoot] = root_type
        self._data: Optional[Dict[Identity, TEntity]] = None

    @property
    def data(self) -> Dict[Identity, TEntity]:
        if self._data is None:
            self.load_data()
        return self._data

    @abstractmethod
    def generate_mapping(self, root_data: TRoot) -> Dict[Identity, TEntity]:
        ...

    @abstractmethod
    def aggregate_root(self, items: Iterable[TEntity]) -> TRoot:
        ...

    @property
    def _file_type(self) -> Literal["json", "yaml"]:
        ext = self.file_path.suffix
        if ext == ".json":
            return "json"
        if ext == ".yaml":
            return "yaml"
        raise NotImplementedError(f"Not sure how to serialize {ext} extension!")

    def load_data(self):
        file_type = self._file_type
        if file_type == "json":
            with open(self.file_path, "r") as f:
                deserialized = json.load(f)
        elif file_type == "yaml":
            yaml = YAML()
            deserialized = yaml.load(self.file_path)
        else:
            raise NotImplementedError(f"Not sure how to dump {file_type} file type")

        root_model = self.root_type(**deserialized)
        self._data = self.generate_mapping(root_model)

    def dump_data(self):
        root_data = self.aggregate_root(self.data.values())
        file_type = self._file_type
        if file_type == "json":
            self.file_path.write_text(root_data.json())
        elif file_type == "yaml":
            self.file_path.write_text(root_data.yaml())
        else:
            raise NotImplementedError(f"Not sure how to dump {file_type} file type")
