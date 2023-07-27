import os

from dotenv import load_dotenv
from s3fs import S3FileSystem

from constants import BUCKET_PHOTO

load_dotenv()

MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
MINIO_PORT = os.getenv('MINIO_PORT')


class AbstractUploader:
    def run(self):
        pass


class MinioUploader(AbstractUploader):
    FILE_SYSTEM = S3FileSystem(key=MINIO_ROOT_USER, secret=MINIO_ROOT_PASSWORD,
                               endpoint_url=f'http://localhost:{MINIO_PORT}')

    def __init__(self, local_path, order_id):
        self.local_path = local_path
        self.order_id = order_id

    # Вопрос Вове почему двойная запись?
    def run(self):
        s3_path = f'{BUCKET_PHOTO}/{self.order_id}'
        # for file in os.listdir(self.local_path):
        self.FILE_SYSTEM.upload(
            str(self.local_path),
            s3_path, recursive=True
        )

        return s3_path
