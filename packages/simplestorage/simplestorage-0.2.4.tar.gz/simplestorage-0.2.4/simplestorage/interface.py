from urllib.parse import urlparse
from typing import List
from io import BytesIO, StringIO
from .clients import LocalStorage, GCStorage
from .templates import DataUnit, StorageBase

network_clients = {
    'gs': GCStorage
}


class StorageInterface(StorageBase):

    def __init__(self):
        self.service = {}

    def _get_service(self, uri: str):
        p = urlparse(uri)

        if p.scheme == '' and p.path == '':
            raise Exception('Invalid uri %s' % uri)

        if p.scheme in network_clients.keys() and p.netloc == '':
            raise Exception('Invalid or unrecognized uri %s' % uri)

        # Load service
        if p.scheme == '' and p.scheme not in self.service.keys():
            self.service[p.scheme] = LocalStorage()
        elif p.scheme not in self.service.keys():
            self.service[p.scheme] = network_clients[p.scheme]()

        return self.service[p.scheme]

    def ls(self, uri: str) -> List[DataUnit]:
        service = self._get_service(uri)
        listing = service.ls(uri=uri)
        return listing

    def save(self, data: bytes, uri: str) -> bool:
        service = self._get_service(uri)
        status = service.save(data=data, uri=uri)
        return status

    def load(self, uri: str) -> BytesIO:
        service = self._get_service(uri)
        f = service.load(uri=uri)
        return f

    def loads(self, uri: str) -> StringIO:
        service = self._get_service(uri)
        f = service.loads(uri=uri)
        return f

    def rm(self, uri: str) -> bool:
        service = self._get_service(uri)
        status = service.rm(uri=uri)
        return status
