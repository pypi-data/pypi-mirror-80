from abc import ABCMeta, abstractmethod
from typing import List
from io import StringIO, BytesIO
from .data import DataUnit


class StorageBase(metaclass=ABCMeta):
    @abstractmethod
    def ls(self, uri: str) -> List[DataUnit]:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: bytes, uri: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def load(self, uri: str) -> BytesIO:
        raise NotImplementedError

    @abstractmethod
    def loads(self, uri: str) -> StringIO:
        raise NotImplementedError

    @abstractmethod
    def rm(self, uri: str) -> bool:
        raise NotImplementedError
