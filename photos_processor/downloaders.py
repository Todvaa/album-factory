import os
import shutil
import tempfile
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from s3fs import S3FileSystem

from constants import BUCKET_PHOTO

load_dotenv()

MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
MINIO_PORT = os.getenv('MINIO_PORT')


class AbstractDownloader(ABC):

    def __init__(self, order_id: int):
        self.order_id = str(order_id)
        self.downloads_dir = os.path.join(tempfile.mkdtemp(''), self.order_id)

    @abstractmethod
    def run(self):
        pass

    def clean(self):
        shutil.rmtree(self.downloads_dir)


class MinioDownloader(AbstractDownloader):
    FILE_SYSTEM = S3FileSystem(
        key=MINIO_ROOT_USER, secret=MINIO_ROOT_PASSWORD,
        endpoint_url=f'http://localhost:{MINIO_PORT}'
    )

    def run(self):
        self.FILE_SYSTEM.get(
            f'{BUCKET_PHOTO}/{self.order_id}/',
            self.downloads_dir, recursive=True
        )

        return
