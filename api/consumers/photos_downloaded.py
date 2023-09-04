import json

from propan.brokers.rabbit import RabbitQueue

from common.models import OrderStatus
from consumers.utils import change_order_status_async
from shared.logger import logger
from shared.queue import exchange, rabbitmq_broker

MODULE_NAME = 'PHOTOS_DOWNLOADED'
photos_downloaded_queue = RabbitQueue('photos_downloaded')


def init():
    pass


@rabbitmq_broker.handle(photos_downloaded_queue, exchange, retry=True)
async def photos_downloaded_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    await change_order_status_async(
        module_name=MODULE_NAME,
        order_id=message['order_id'],
        new_status=OrderStatus.portraits_processing.name
    )
