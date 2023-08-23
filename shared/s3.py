import os

from dotenv import load_dotenv
from s3fs import S3FileSystem

load_dotenv()

S3_ROOT_USER = os.getenv('S3_ROOT_USER')
S3_ROOT_PASSWORD = os.getenv('S3_ROOT_PASSWORD')
S3_URL = os.getenv('S3_URL')

PREVIEW_DIR = 'preview'
SMALL_PH = 'small'
LARGE_PH = 'large'
ORIGINAL_PH = 'original'

FILE_SYSTEM = S3FileSystem(
    key=S3_ROOT_USER, secret=S3_ROOT_PASSWORD,
    endpoint_url=S3_URL
)

BUCKET_PHOTO = 'photos-storage'

ALLOWED_SIZES = (SMALL_PH, LARGE_PH, ORIGINAL_PH)


def get_photo_url(order_id: int, photo_name: str, size: str) -> str:
    s3_path = f'{BUCKET_PHOTO}/{order_id}/'
    if size not in ALLOWED_SIZES:
        raise ValueError(f'Invalid size. Allowed: {ALLOWED_SIZES}')
    if size == ORIGINAL_PH:
        s3_path += f'{size}/{photo_name}/'
    else:
        s3_path += f'{PREVIEW_DIR}/{size}/{photo_name}/'

    return s3_path
