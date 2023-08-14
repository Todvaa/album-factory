import os
import shutil
import tempfile
from abc import ABC, abstractmethod

from constants import MODULE_NAME
from shared.logger import logger
from shared.s3 import FILE_SYSTEM


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
    file_system = FILE_SYSTEM

    def run(self) -> str:
        logger.info(module=MODULE_NAME, message='start downloading from S3')
        self.file_system.get(
            self.s3_path,
            self.downloads_dir, recursive=True
        )
        logger.info(module=MODULE_NAME, message='photos downloaded')

        return self.downloads_dir
