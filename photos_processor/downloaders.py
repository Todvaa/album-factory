import os
import shutil
import tempfile
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from s3fs import S3FileSystem

from constants import ORIG_PH_DIR

load_dotenv()

MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
MINIO_PORT = os.getenv('MINIO_PORT')


class AbstractDownloader(ABC):

    def __init__(self, order_id: int, s3_path: str):
        self.order_id = str(order_id)
        self.s3_path = s3_path + f'{self.order_id}/{ORIG_PH_DIR}/'
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

    def run(self) -> str:
        self.FILE_SYSTEM.get(
            self.s3_path,
            self.downloads_dir, recursive=True
        )

        return self.downloads_dir
