from asgiref.sync import sync_to_async

from common.models import Order
from shared.logger import logger


def change_order_status(module_name, order_id, new_status):
    try:
        order = Order.objects.get(id=order_id)
        logger.info(
            module=module_name, message='Order successfully found by ID'
        )
        order.status = new_status
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


change_order_status_async = sync_to_async(change_order_status)
