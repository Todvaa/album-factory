import asyncio
import json

from propan.brokers.rabbit import RabbitQueue

from common.models import Order, OrderStatus
from constants import MODULE_NAME
from shared.logger import logger
from shared.queue import exchange, rabbitmq_broker, app

photos_downloaded_queue = RabbitQueue('photos_downloaded')


@rabbitmq_broker.handle(photos_downloaded_queue, exchange, retry=True)
async def photos_downloaded_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    try:
        logger.info(
            module=MODULE_NAME, message='Order successfully found by ID'
        )
        order = Order.objects.get(id=message['order_id'])
        order.status = OrderStatus.portraits_uploaded.name
        order.save()
        logger.info(
            module=MODULE_NAME,
            message=(
                f'The status of order №{order.id} has'
                f' been successfully changed to{order.status}'
            )
        )
    except Order.DoesNotExist as error:
        logger.info(
            module=MODULE_NAME,
            message=f'Could not find order by ID. Error{str(error)}'
        )


if __name__ == "__main__":
    asyncio.run(app.run())
