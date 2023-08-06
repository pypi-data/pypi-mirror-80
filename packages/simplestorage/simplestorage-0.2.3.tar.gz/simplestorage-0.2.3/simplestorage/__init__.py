from io import BytesIO, StringIO
from .interface import StorageInterface

interface_session = StorageInterface()


def ls(uri: str):
    return interface_session.ls(uri=uri)


def save(data: bytes, uri: str):
    return interface_session.save(data=data, uri=uri)


def load(data: bytes, uri: str) -> BytesIO:
    return interface_session.load(uri=uri)


def loads(uri: str) -> StringIO:
    return interface_session.loads(uri=uri)


def delete(uri: str) -> bool:
    return interface_session.delete(uri=uri)


def rm(uri: str) -> bool:
    return interface_session.delete(uri=uri)
