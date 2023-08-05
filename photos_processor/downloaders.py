import os
import shutil
import tempfile
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from s3fs import S3FileSystem

from constants import MODULE_NAME
from shared.logger import logger

load_dotenv()

S3_ROOT_USER = os.getenv('S3_ROOT_USER')
S3_ROOT_PASSWORD = os.getenv('S3_ROOT_PASSWORD')
S3_URL = os.getenv('S3_URL')


class AbstractDownloader(ABC):

    def __init__(self, order_id: int, s3_path: str):
        self.order_id = str(order_id)
        self.s3_path = s3_path
        self.downloads_dir = os.path.join(tempfile.mkdtemp(''), self.order_id)

    @abstractmethod
    def run(self):
        pass

    def clean(self):
        shutil.rmtree(self.downloads_dir)


class S3Downloader(AbstractDownloader):
    FILE_SYSTEM = S3FileSystem(
        key=S3_ROOT_USER, secret=S3_ROOT_PASSWORD,
        endpoint_url=S3_URL
    )

    def run(self) -> str:
        logger.info(module=MODULE_NAME, message='start downloading from S3')
        self.FILE_SYSTEM.get(
            self.s3_path,
            self.downloads_dir, recursive=True
        )
        logger.info(module=MODULE_NAME, message='photos downloaded')

        return self.downloads_dir
