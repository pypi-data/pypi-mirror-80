from abc import ABC
from typing import Dict, Generic, Iterable, NoReturn, Optional, Type, TypeVar

from pydantic import BaseModel, FilePath

from autogram_commons.entity_repository_base import EntityRepositoryBase
from autogram_commons.filedataloader import FileDataLoader
from autogram_commons.identifiable import IdentifiableBaseModel, Identity


TEntity = TypeVar("TEntity", bound=IdentifiableBaseModel, covariant=True)
TRoot = TypeVar("TRoot", bound=BaseModel)


class FileEntityRepository(
    # XXX: Do the generics need to be repeated?
    EntityRepositoryBase[TEntity],
    FileDataLoader[TEntity, TRoot],
    Generic[TEntity, TRoot],
    ABC,
):
    def __init__(self, file_path: FilePath, entity_type: Type[TEntity], root_type: Type[TRoot]):
        super().__init__(file_path=file_path, root_type=root_type)
        self.entity_type = entity_type

    def generate_json_schema(self) -> str:
        return self.root_type.schema_json()

    def write_json_schema(self, to: FilePath = None) -> NoReturn:
        """
        Writes the associated model's JSON schema to the specified path, or next to the data file if `None` is passed.
        """
        schema = self.generate_json_schema()
        to = to or self.file_path.with_suffix(".schema.json")
        to.write_text(schema, "utf-8")

    def iter(self) -> Iterable[TEntity]:
        return self.data.values()

    def get_by_id(self, identity: Identity) -> TEntity:
        return self.data[identity]

    def get_by_id_or_none(self, identity: Identity, raise_: bool = False) -> Optional[TEntity]:
        return self.data.get(identity, None)

    def update(self, identity: Identity, values: Dict = None, **kwargs) -> TEntity:
        if values:
            kwargs.update(values)
        d = self.get_by_id(identity)

        to_update = {}
        for k, v in d.dict():
            to_update[k] = kwargs[k] if k in kwargs else v

        result = self.entity_type(**to_update)
        self.data[identity] = result
        return result
