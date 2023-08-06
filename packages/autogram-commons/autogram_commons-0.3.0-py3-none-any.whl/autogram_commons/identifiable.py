from abc import ABC, abstractmethod

from pydantic import BaseModel, constr

Identity = constr(strip_whitespace=True, strict=True, min_length=2, regex=r"[a-z-]*")


class Identifiable(ABC):
    @property
    @abstractmethod
    def identity(self) -> Identity:
        ...


class IdentifiableBaseModel(BaseModel, Identifiable, ABC):
    def __hash__(self) -> int:
        return hash(self.identity)
