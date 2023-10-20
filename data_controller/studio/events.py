import asyncio
import json
from abc import ABC, abstractmethod

from propan.brokers.rabbit import RabbitQueue

from shared.queue import exchange, get_rabbitmq_broker


class AbstractEvent(ABC):
    rabbitmq_broker = get_rabbitmq_broker()

    @abstractmethod
    def handle(self):
        pass

    def _serialize(self, **kwargs) -> str:
        return json.dumps(kwargs)


class PhotosUploadingEvent(AbstractEvent):
    exchange = exchange
    photos_downloading_queue = RabbitQueue('photos_downloading')

    def __init__(self, url: str, order_id: int):
        self.url = url
        self.order_id = order_id

    async def queue(self):
        async with self.rabbitmq_broker as broker:
            await broker.publish(
                message=self._serialize(
                    url=self.url, order_id=self.order_id
                ),
                exchange=self.exchange, routing_key='photos_downloading'
            )

    def handle(self):
        asyncio.run(self.queue())
