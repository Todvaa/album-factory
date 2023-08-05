import asyncio
import json
import os

from dotenv import load_dotenv
from propan import RabbitBroker, PropanApp
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

from classificators import Classificator
from downloaders import S3Downloader
from dto import Photo
from photos_processor.constants import ORIG_PH_DIR
from recognizers import Recognizer

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
broker = RabbitBroker(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost:{RABBITMQ_PORT}/')
app = PropanApp(broker)
exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)

photos_processing_queue = RabbitQueue('photos_processing')
photos_processed_queue = RabbitQueue('photos_processed')


# todo: добавить логи
@broker.handle(photos_processing_queue, exchange, retry=True)
async def photos_processing_handler(message):
    message = json.loads(message)
    order_id = message['order_id']
    s3_path = message['s3_path'] + f'{order_id}/{ORIG_PH_DIR}/'
    downloader = S3Downloader(order_id=order_id, s3_path=s3_path)
    local_path = downloader.run()
    photos = [
        Photo(name=name).set_remote_url(
            remote_url=s3_path + name
        ) for name in os.listdir(local_path)
    ]
    recognizer = Recognizer(dir_path=local_path, photos=photos)
    persons_vectors = recognizer.run()
    downloader.clean()
    classificator = Classificator(vectors=persons_vectors)
    persons = classificator.run()
    data = {
        'order_id': order_id,
        'images': [
            {
                's3_url': photo.remote_url, 'face_count': photo.face_count
            } for photo in photos
        ],
        'persons': persons
    }

    await publish_vectors(data)


async def publish_vectors(data):
    async with RabbitBroker(
            f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}'
            f'@localhost:{RABBITMQ_PORT}/'
    ) as br:
        await br.publish(
            message=json.dumps(data),
            exchange=exchange, routing_key='photos_processed'
        )


if __name__ == "__main__":
    asyncio.run(app.run())
