from typing import Union, Iterable

import backoff
from google.cloud.storage import Client as GoogleStorageClient, Blob

from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY


class Client(GoogleStorageClient):
    def __init__(self, project=None, credentials=None, _http=None):
        super().__init__(project=project, credentials=credentials, _http=_http)

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def list_blobs(self, bucket_name: str, prefix: Union[str, None] = None) -> Iterable[Blob]:
        bucket = self.get_bucket(bucket_name)
        return bucket.list_blobs(prefix=prefix)

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def list_gcs_directories(self, bucket_name: str, prefix: str = None):
        """
            Get subdirectories of a "folder"
        :param bucket:
        :param prefix:
        :return list of "directories":
        """
        # from https://github.com/GoogleCloudPlatform/google-cloud-python/issues/920
        bucket = self.get_bucket(bucket_name)
        if prefix:
            if prefix[-1] != '/':
                prefix += '/'
        iterator = bucket.list_blobs(prefix=prefix, delimiter='/')
        prefixes = set()
        for page in iterator.pages:
            prefixes.update(page.prefixes)
        return [directory.strip(prefix).strip('/') for directory in prefixes]

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def get_blob(self, bucket_name: str, file_name: str) -> Blob:
        bucket = self.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        return blob
