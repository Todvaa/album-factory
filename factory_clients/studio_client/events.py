import asyncio
import json
import os

from dotenv import load_dotenv
from propan import RabbitBroker
from propan.brokers.rabbit import RabbitExchange, ExchangeType, RabbitQueue

load_dotenv()


class AbstractEvent:
    RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
    RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
    # todo: move port to env
    broker = RabbitBroker(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost:5672/')

    # todo: decorator
    def handle(self):
        pass

    def _serialize(self, **kwargs):
        return json.dumps(kwargs)


class PhotosUploadingEvent(AbstractEvent):
    exchange = RabbitExchange('upload_photo_exchange', type=ExchangeType.DIRECT)
    upload_photo_queue = RabbitQueue('upload_photo')

    def __init__(self, url, order_id):
        self.url = url
        self.order_id = order_id

    async def queue(self):
        async with self.broker as broker:
            await broker.publish(
                message=self._serialize(
                    url=self.url, order_id=self.order_id
                ),
                exchange=self.exchange, routing_key='upload_photo'
            )

    def handle(self):
        asyncio.run(self.queue())
