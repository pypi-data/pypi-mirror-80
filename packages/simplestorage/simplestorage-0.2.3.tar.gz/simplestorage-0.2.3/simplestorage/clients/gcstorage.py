from io import BytesIO, StringIO
from typing import List
from urllib.parse import urlparse
from google.cloud import storage
from ..templates import StorageBase, DataUnit


class GCStorage(StorageBase):
    def __init__(self, project: str = None):
        self.storage_client = storage.Client(project=project)

    def ls(self, uri: str) -> List[DataUnit]:
        elements = self._list_blobs(uri=uri)
        return elements

    def save(self, data: bytes, uri: str) -> bool:
        done = self._upload_blob(data=data, uri=uri)
        return done

    def load(self, uri: str) -> BytesIO:
        f = self._download_to_memory(uri)
        return f

    def loads(self, uri: str) -> StringIO:
        byte_stream = self._download_to_memory(uri)
        str_obj = byte_stream.read().decode('utf-8')
        string_stream = StringIO(str_obj)

        return string_stream

    def delete(self, uri: str) -> bool:
        blob = self._get_blob(uri)
        blob.delete()

        return True

    def _download_to_memory(self, uri: str) -> BytesIO:
        blob = self._get_blob(uri)

        byte_stream = BytesIO()
        blob.download_to_file(byte_stream)
        byte_stream.seek(0)

        return byte_stream

    def _get_blob(self, uri: str):
        parsed_url = self._parse_uri(uri)
        bucket_name, prefix = self._get_bucket_prefix(parsed_url)

        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(prefix)

        return blob

    def _parse_uri(self, uri: str):
        if uri[-1] == '/':
            uri = uri[:-1]

        p = urlparse(uri)

        if p.scheme != 'gs' or p.netloc == '':
            raise Exception('Invalid URI: %s' % uri)

        return p

    def _get_bucket_prefix(self, parsed_url):
        bucket_name = parsed_url.netloc
        prefix = parsed_url.path

        if prefix != '' and prefix[0] == '/':
            prefix = prefix[1:]

        return bucket_name, prefix

    def _upload_blob(self, data: bytes, uri: str):
        f = BytesIO(data)
        f.seek(0)

        blob = self._get_blob(uri)
        blob.upload_from_file(f)

        return True

    def _list_blobs(self, uri: str, delimiter='/') -> List[DataUnit]:
        parsed_url = self._parse_uri(uri)
        bucket_name, prefix = self._get_bucket_prefix(parsed_url)

        if prefix:
            if prefix[-1] != '/':
                prefix = prefix + '/'

        blobs = self.storage_client.list_blobs(
            bucket_name, prefix=prefix, delimiter=delimiter
        )

        path_objects = [
            DataUnit(
                name=blb.name.replace(prefix, ''),
                uri=f"gs://{bucket_name}/{prefix}{blb.name.replace(prefix, '')}",
                is_folder=False)
            for page in blobs.pages for blb in page]

        path_prefixes = [DataUnit(name=pref.replace(prefix, '')[:-1],
                                  uri=f"gs://{bucket_name}/{pref[:-1]}",
                                  is_folder=True)
                         for pref in blobs.prefixes]

        return path_objects + path_prefixes
