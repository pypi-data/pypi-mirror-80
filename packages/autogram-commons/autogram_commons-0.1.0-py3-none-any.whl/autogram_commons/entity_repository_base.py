from abc import ABC, abstractmethod
from typing import Callable, Dict, Generic, Iterator, List, Optional, TypeVar

from autogram_commons.identifiable import Identifiable, Identity

T = TypeVar("T", bound=Identifiable)


class EntityRepositoryBase(Generic[T], ABC):
    @abstractmethod
    def iter(self) -> Iterator[T]:
        ...

    def list_items(self) -> List[T]:
        return list(self.iter())

    def filter(self, predicate: Callable[[T], bool]) -> Iterator[T]:
        return filter(predicate, self.iter())

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        return next(self.filter(predicate), None)

    @abstractmethod
    def get_by_id(self, identity: Identity) -> T:
        ...

    @abstractmethod
    def get_by_id_or_none(self, identity: Identity, raise_: bool = False) -> Optional[T]:
        ...

    @abstractmethod
    def update(self, identity: Identity, values: Dict = None, **kwargs) -> T:
        ...
