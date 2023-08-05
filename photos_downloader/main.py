import asyncio
import json
import os

from dotenv import load_dotenv
from propan import RabbitBroker, PropanApp
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

from downloaders import YandexDownloader
from photos_downloader.constants import MODULE_NAME
from photos_downloader.uploaders import S3Uploader
from shared.logger import logger

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
rabbitmq_broker = RabbitBroker(
    f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}'
    f'@localhost:{RABBITMQ_PORT}/'
)
app = PropanApp(rabbitmq_broker)
exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)

photos_downloading_queue = RabbitQueue('photos_downloading')
photos_downloaded_queue = RabbitQueue('photos_downloaded')
photos_processing_queue = RabbitQueue('photos_processing')


# todo: For more complex use-cases just use the tenacity library for retry.
@rabbitmq_broker.handle(photos_downloading_queue, exchange, retry=True)
async def photos_downloading_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    order_id = message['order_id']
    downloader = YandexDownloader(
        source=message['url'],
        order_id=order_id
    )
    local_path = downloader.run()
    s3_path = S3Uploader(
        local_path=local_path,
    ).run()
    logger.info(module=MODULE_NAME, message=f's3 path: {s3_path}')
    downloader.clean()
    await publish_photos(order_id, s3_path)
    logger.info(module=MODULE_NAME, message=f'message handled')


async def publish_photos(order_id, s3_path):
    async with RabbitBroker(
            f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}'
            f'@localhost:{RABBITMQ_PORT}/'
    ) as broker:
        logger.info(
            module=MODULE_NAME,
            message=f'pushing message to {photos_downloaded_queue.name}'
        )
        await broker.publish(
            message=json.dumps({'order_id': order_id, 's3_path': s3_path}),
            exchange=exchange, routing_key='photos_downloaded'
        )
        logger.info(
            module=MODULE_NAME,
            message=f'pushing message to {photos_processing_queue.name}'
        )
        await broker.publish(
            message=json.dumps({'order_id': order_id, 's3_path': s3_path}),
            exchange=exchange, routing_key='photos_processing'
        )
    logger.info(
        module=MODULE_NAME, message=f'pushed'
    )

if __name__ == '__main__':
    asyncio.run(app.run())
