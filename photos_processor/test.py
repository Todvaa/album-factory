import asyncio
import json
import os

from dotenv import load_dotenv
from propan import RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)

photos_processing_queue = RabbitQueue('photos_processing')


async def publish_photos(order_id, s3_path):
    async with RabbitBroker(
            f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}'
            f'@localhost:{RABBITMQ_PORT}/'
    ) as br:
        await br.publish(
            message=json.dumps({'order_id': order_id, 's3_path': s3_path}),
            exchange=exchange, routing_key='photos_processing'
        )


if __name__ == '__main__':
    asyncio.run(publish_photos(order_id=2, s3_path='photos-storage/'))
