import os

from dotenv import load_dotenv
from s3fs import S3FileSystem

from constants import SM_PH_DIR, LG_PH_DIR, ORIG_PH_DIR

load_dotenv()

MINIO_PORT = os.getenv('MINIO_PORT')


class AbstractUploader:
    def run(self):
        pass


class MinioUploader(AbstractUploader):
    FILE_SYSTEM = S3FileSystem(endpoint_url=f'localhost:{MINIO_PORT}')

    def __init__(self, local_path, order_id):
        self.local_path = local_path
        self.order_id = order_id

    def run(self):
        for folder_name in SM_PH_DIR, LG_PH_DIR:
            for file in os.listdir(self.local_path / folder_name):
                self.FILE_SYSTEM.upload(
                    os.path.join(self.local_path, folder_name, file),
                    f'/{self.order_id}/preview/{folder_name}/{file}'
                )
        for file in os.listdir(self.local_path / ORIG_PH_DIR):
            self.FILE_SYSTEM.upload(
                os.path.join(self.local_path, ORIG_PH_DIR, file),
                f'/{self.order_id}/{ORIG_PH_DIR}/{file}'
            )

        return
