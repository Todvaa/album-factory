import asyncio
import json
import os

from dotenv import load_dotenv
from propan import RabbitBroker, PropanApp
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

from downloaders import YandexDownloader
from photos_downloader.uploaders import MinioUploader

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
broker = RabbitBroker(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost:5672/')
app = PropanApp(broker)
exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)

photo_downloading_queue = RabbitQueue('photo_downloading')
photos_downloaded_queue = RabbitQueue('photos_downloaded')
photo_processing_queue = RabbitQueue('photo_processing')


@broker.handle(photo_downloading_queue, exchange, retry=True)
async def photo_downloading_handler(message):
    # For more complex usecases just use the tenacity library.
    # возвращает тип данных WindowsPath
    message = json.loads(message)
    order_id = str(message['order_id'])
    downloader = YandexDownloader(
        source=message['url'],
        order_id=order_id
    )
    # 'C:\\Users\\mi\\AppData\\Local\\Temp\\tmp7b40nxdo\\2\\
    local_path = downloader.run()
    s3_path = MinioUploader(
        local_path=local_path,
        order_id=order_id
    ).run()
    # todo: проверить почему директория не удалилась
    downloader.clean()

    async with broker:
        await broker.publish(
            message=json.dumps({'order_id': order_id, 's3_path': s3_path}),
            exchange=exchange, routing_key='photos_downloaded'
        )
    async with broker:
        await broker.publish(
            message=json.dumps({'order_id': order_id, 's3_path': s3_path}),
            exchange=exchange, routing_key='photo_processing'
        )

if __name__ == '__main__':
    asyncio.run(app.run())
