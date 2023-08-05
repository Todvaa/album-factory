import os
import re
import shutil
import tempfile
from abc import ABC, abstractmethod
from typing import List
from urllib.parse import urlparse, parse_qsl, urlencode

import requests
from slugify import slugify

from constants import (
    SM_PH_DIR, LG_PH_DIR, ORIG_PH_DIR, SM_PH_SZ, LG_PH_SZ, PREVIEW_DIR, MODULE_NAME
)
from shared.logger import logger


class AbstractDownloader(ABC):

    # source is cloud url
    def __init__(self, source: str, order_id: int):
        self.source = source
        self.order_id = str(order_id)
        self.downloads_dir = os.path.join(tempfile.mkdtemp(''), self.order_id)

    @abstractmethod
    def run(self):
        pass

    def clean(self):
        shutil.rmtree(self.downloads_dir)


class YandexDownloader(AbstractDownloader):
    # test cloud https://disk.yandex.ru/d/RTqLhx3YnUxUrQ
    API_METHOD = f'https://cloud-api.yandex.net/v1/disk/public/resources'

    def __get_photos_data(self) -> List[dict]:
        response = requests.get(url=f'{self.API_METHOD}?public_key={self.source}')
        if response.status_code != 200:
            raise ValueError('Yandex API request was not successful.')

        return response.json()['_embedded']['items']

    def __change_size(self, photo_url: str, new_size: str) -> str:
        parsed_url = urlparse(photo_url)
        query_params = dict(parse_qsl(parsed_url.query))
        query_params['size'] = new_size

        return parsed_url._replace(query=urlencode(query_params)).geturl()

    def __change_name(self, current_name: str) -> str:
        pattern = r'(?P<base_name>.+)\.(?P<extension>[^.]+)$'
        match = re.match(pattern, current_name)
        base_name = match.group('base_name')
        extension = match.group('extension')
        while base_name + '.' + extension in os.path.join(self.downloads_dir, ORIG_PH_DIR):
            base_name = base_name + '-'

        return slugify(base_name) + '.' + extension

    # todo: mock тест
    def __download_content(self, url: str) -> bytes:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError('Failed to download content.')

    def run(self) -> str:
        logger.info(module=MODULE_NAME, message='start downloading from Yandex')
        os.mkdir(self.downloads_dir)
        preview_dir = os.path.join(self.downloads_dir, PREVIEW_DIR)
        os.mkdir(preview_dir)
        small_dir = os.path.join(preview_dir, SM_PH_DIR)
        os.mkdir(small_dir)
        large_dir = os.path.join(preview_dir, LG_PH_DIR)
        os.mkdir(large_dir)
        original_dir = os.path.join(self.downloads_dir, ORIG_PH_DIR)
        os.mkdir(original_dir)
        photos_data = self.__get_photos_data()
        for photo_data in photos_data:
            logger.info(
                module=MODULE_NAME, message=f'downloading photo {photo_data["preview"]}'
            )
            small_photo = self.__download_content(
                self.__change_size(photo_url=photo_data['preview'], new_size=SM_PH_SZ)
            )
            large_photo = self.__download_content(
                self.__change_size(photo_url=photo_data['preview'], new_size=LG_PH_SZ)
            )
            original_photo = self.__download_content(photo_data['file'])
            photo_name = self.__change_name(current_name=photo_data['name'])
            with open(os.path.join(small_dir, photo_name), 'wb') as file:
                file.write(small_photo)
            with open(os.path.join(large_dir, photo_name), 'wb') as file:
                file.write(large_photo)
            with open(os.path.join(original_dir, photo_name), 'wb') as file:
                file.write(original_photo)
        logger.info(
            module=MODULE_NAME,
            message=f'{len(photos_data) * 3} photos downloaded'
        )

        return self.downloads_dir
