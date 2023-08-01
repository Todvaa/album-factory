#
from downloaders import YandexDownloader
from uploaders import MinioUploader

x = YandexDownloader(source='https://disk.yandex.ru/d/RTqLhx3YnUxUrQ', order_id=2)
x.run()

local_path = 'C:\\Users\\mi\\AppData\\Local\\Temp\\tmp7b40nxdo\\2'
order_id = MinioUploader(
    local_path=local_path
).run()
