from common.models import Order, OrderStatus
from shared.logger import logger


class OrderDataStorage:
    @staticmethod
    def change_status(order: Order, status: OrderStatus):
        order.status = status.name
        order.full_clean()
        order.save()
        logger.info(
            module=OrderDataStorage.__name__,
            message=(
                f'the status of order №{order.id} has'
                f' been successfully changed to {order.status}'
            )
        )
