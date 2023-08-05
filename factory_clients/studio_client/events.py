import asyncio
import json
import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from propan import RabbitBroker
from propan.brokers.rabbit import RabbitExchange, ExchangeType, RabbitQueue

load_dotenv()


class AbstractEvent(ABC):
    RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
    RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    broker = RabbitBroker(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost:{RABBITMQ_PORT}/')

    @abstractmethod
    def handle(self):
        pass

    def _serialize(self, **kwargs) -> str:
        return json.dumps(kwargs)


class PhotosUploadingEvent(AbstractEvent):
    exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)
    photos_downloading_queue = RabbitQueue('photos_downloading')

    def __init__(self, url: str, order_id: int):
        self.url = url
        self.order_id = order_id

    async def queue(self):
        async with self.broker as broker:
            await broker.publish(
                message=self._serialize(
                    url=self.url, order_id=self.order_id
                ),
                exchange=self.exchange, routing_key='photos_downloading'
            )

    def handle(self):
        asyncio.run(self.queue())
