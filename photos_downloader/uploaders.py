import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from s3fs import S3FileSystem

from constants import BUCKET_PHOTO, MODULE_NAME
from shared.logger import logger

load_dotenv()

S3_ROOT_USER = os.getenv('S3_ROOT_USER')
S3_ROOT_PASSWORD = os.getenv('S3_ROOT_PASSWORD')
S3_URL = os.getenv('S3_URL')


class AbstractUploader(ABC):

    @abstractmethod
    def run(self):
        pass


class S3Uploader(AbstractUploader):
    FILE_SYSTEM = S3FileSystem(
        key=S3_ROOT_USER, secret=S3_ROOT_PASSWORD,
        endpoint_url=S3_URL
    )

    def __init__(self, local_path: str):
        self.local_path = local_path

    def run(self) -> str:
        logger.info(module=MODULE_NAME, message='start uploading to s3')

        s3_path = f'{BUCKET_PHOTO}/'
        self.FILE_SYSTEM.upload(
            self.local_path,
            s3_path, recursive=True
        )
        logger.info(module=MODULE_NAME, message='uploaded')

        return s3_path
