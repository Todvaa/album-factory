import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from s3fs import S3FileSystem

from constants import BUCKET_PHOTO, MODULE_NAME
from shared.logger import logger

load_dotenv()

MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
MINIO_PORT = os.getenv('MINIO_PORT')


class AbstractUploader(ABC):

    @abstractmethod
    def run(self):
        pass


class MinioUploader(AbstractUploader):
    FILE_SYSTEM = S3FileSystem(
        key=MINIO_ROOT_USER, secret=MINIO_ROOT_PASSWORD,
        endpoint_url=f'http://localhost:{MINIO_PORT}'
    )

    def __init__(self, local_path: str):
        self.local_path = local_path

    def run(self) -> str:
        logger.info(module=MODULE_NAME, message='start uploading to s3')

        s3_path = f'{BUCKET_PHOTO}/'
        self.FILE_SYSTEM.upload(
            str(self.local_path),
            s3_path, recursive=True
        )
        logger.info(module=MODULE_NAME, message='uploaded')

        return s3_path
