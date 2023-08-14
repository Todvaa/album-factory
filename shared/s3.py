import os

from dotenv import load_dotenv
from s3fs import S3FileSystem

load_dotenv()

S3_ROOT_USER = os.getenv('S3_ROOT_USER')
S3_ROOT_PASSWORD = os.getenv('S3_ROOT_PASSWORD')
S3_URL = os.getenv('S3_URL')

FILE_SYSTEM = S3FileSystem(
    key=S3_ROOT_USER, secret=S3_ROOT_PASSWORD,
    endpoint_url=S3_URL
)
