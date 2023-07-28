import os
import tempfile
from urllib.parse import urlparse, parse_qsl, urlencode

import requests

from constants import (
    SM_PH_DIR, LG_PH_DIR, ORIG_PH_DIR, SM_PH_SZ, LG_PH_SZ, PREVIEW_DIR
)


class AbstractDownloader:

    def __init__(self, source, order_id):
        self.source = source
        self.order_id = order_id
        self.downloads_dir = os.path.join(tempfile.mkdtemp(''), order_id)

    # метод должен возращать пути до локальной директории, куда он все скачал
    def run(self):
        pass

    def clean(self):
        os.rmdir(self.downloads_dir)


class YandexDownloader(AbstractDownloader):
    # тестовое облако https://disk.yandex.ru/d/RTqLhx3YnUxUrQ
    API_METHOD = f'https://cloud-api.yandex.net/v1/disk/public/resources'

    def __get_photos_data(self):
        response = requests.get(url=f'{self.API_METHOD}?public_key={self.source}')
        if response.status_code != 200:
            raise ValueError('Yandex API request was not successful.')

        return response.json()['_embedded']['items']

    def __change_size(self, photo_url, new_size):
        parsed_url = urlparse(photo_url)
        query_params = dict(parse_qsl(parsed_url.query))
        query_params['size'] = new_size

        return parsed_url._replace(query=urlencode(query_params)).geturl()

    # todo: mock тест
    def __download_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError('Failed to download content.')

    def run(self):
        photos_data = self.__get_photos_data()
        # todo: check if exist dont reupload
        os.mkdir(self.downloads_dir)
        preview_dir = os.path.join(self.downloads_dir, PREVIEW_DIR)
        os.mkdir(preview_dir)
        small_dir = os.path.join(preview_dir, SM_PH_DIR)
        os.mkdir(small_dir)
        large_dir = os.path.join(preview_dir, LG_PH_DIR)
        os.mkdir(large_dir)
        original_dir = os.path.join(self.downloads_dir, ORIG_PH_DIR)
        os.mkdir(original_dir)
        for photo_data in photos_data:
            small_photo = self.__download_content(
                self.__change_size(photo_url=photo_data['preview'], new_size=SM_PH_SZ)
            )
            large_photo = self.__download_content(
                self.__change_size(photo_url=photo_data['preview'], new_size=LG_PH_SZ)
            )
            original_photo = self.__download_content(photo_data['file'])
            with open(os.path.join(small_dir, photo_data['name']), 'wb') as file:
                file.write(small_photo)
            with open(os.path.join(large_dir, photo_data['name']), 'wb') as file:
                file.write(large_photo)
            with open(os.path.join(original_dir, photo_data['name']), 'wb') as file:
                file.write(original_photo)

        return self.downloads_dir
