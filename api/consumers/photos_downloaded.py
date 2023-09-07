import json

from asgiref.sync import sync_to_async
from propan.brokers.rabbit import RabbitQueue

from common.data_storages import OrderDataStorage
from common.models import OrderStatus, Order
from shared.logger import logger
from shared.queue import (
    exchange, rabbitmq_broker, RETRY_COUNT
)

MODULE_NAME = 'CONSUMER_PHOTOS_DOWNLOADED'
photos_downloaded_queue = RabbitQueue('photos_downloaded')


def init():
    pass


def handle(message: dict):
    order = Order.objects.get(id=message['order_id'])
    OrderDataStorage.change_status(
        order=order,
        status=OrderStatus.portraits_processing,
    )


handle_async = sync_to_async(handle)


@rabbitmq_broker.handle(photos_downloaded_queue, exchange, retry=RETRY_COUNT)
async def photos_downloaded_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    await handle_async(
        message=message
    )
