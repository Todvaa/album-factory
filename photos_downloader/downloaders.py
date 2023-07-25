from urllib.parse import urlparse, parse_qsl, urlencode

import requests

from constants import BASE_DIR, SM_PH_DIR, LG_PH_DIR, ORIG_PH_DIR


class AbstractDownloader:
    SOURCE = None

    # метод должен возращать пути до локальной директории, куда он все скачал
    def run(self):
        pass


class YandexDownloader(AbstractDownloader):
    # тестовое облако https://disk.yandex.ru/d/RTqLhx3YnUxUrQ
    SOURCE = f'https://cloud-api.yandex.net/v1/disk/public/resources'

    def __init__(self, disk_url):
        self.source = f'{self.SOURCE}?public_key={disk_url}'

    def get_photos_data(self):
        response = requests.get(url=self.source)
        if response.status_code != 200:
            raise ValueError('Yandex API request was not successful.')

        return response.json()['_embedded']['items']

    def change_size(self, photo_url, new_size):
        parsed_url = urlparse(photo_url)
        query_params = dict(parse_qsl(parsed_url.query))
        query_params['size'] = new_size

        return parsed_url._replace(query=urlencode(query_params)).geturl()

    # todo: mock тест
    def download_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError('Failed to download content.')

    def run(self):
        photos_data = self.get_photos_data()
        downloads_dir = BASE_DIR / 'downloads'
        downloads_dir.mkdir(exist_ok=True)
        small_dir = downloads_dir / SM_PH_DIR
        small_dir.mkdir(exist_ok=True)
        large_dir = downloads_dir / LG_PH_DIR
        large_dir.mkdir(exist_ok=True)
        original_dir = downloads_dir / ORIG_PH_DIR
        original_dir.mkdir(exist_ok=True)
        for photo_data in photos_data:
            small_photo = self.download_content(
                self.change_size(photo_url=photo_data['preview'], new_size='L')
            )
            large_photo = self.download_content(
                self.change_size(photo_url=photo_data['preview'], new_size='XL')
            )
            original_photo = self.download_content(photo_data['file'])
            with open(small_dir / photo_data['name'], 'wb') as file:
                file.write(small_photo)
            with open(large_dir / photo_data['name'], 'wb') as file:
                file.write(large_photo)
            with open(original_dir / photo_data['name'], 'wb') as file:
                file.write(original_photo)

        return downloads_dir
