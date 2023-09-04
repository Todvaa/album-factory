from common.models import Order, OrderStatus
from shared.logger import logger


class OrderDataStorage:
    @staticmethod
    def change_status(order: Order, status: OrderStatus, module_name: str):
        try:
            logger.info(
                module=module_name, message='Order successfully found by ID'
            )
            order.status = status.name
            order.full_clean()
            order.save()
            logger.info(
                module=module_name,
                message=(
                    f'The status of order №{order.id} has'
                    f' been successfully changed to {order.status}'
                )
            )
        except Order.DoesNotExist as error:
            logger.info(
                module=module_name,
                message=f'Could not find order by ID. Error{str(error)}'
            )
