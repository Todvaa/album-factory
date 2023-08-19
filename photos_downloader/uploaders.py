from abc import ABC, abstractmethod

from photos_downloader.constants import MODULE_NAME
from shared.logger import logger
from shared.s3 import FILE_SYSTEM, BUCKET_PHOTO


class AbstractUploader(ABC):

    @abstractmethod
    def run(self):
        pass


class S3Uploader(AbstractUploader):
    file_system = FILE_SYSTEM

    def __init__(self, local_path: str):
        self.local_path = local_path

    def run(self) -> str:
        logger.info(module=MODULE_NAME, message='start uploading to s3')

        s3_path = f'{BUCKET_PHOTO}/'
        self.file_system.upload(
            self.local_path,
            s3_path, recursive=True
        )
        logger.info(module=MODULE_NAME, message='uploaded')

        return s3_path
