import json

from propan.brokers.rabbit import RabbitQueue

from common.models import OrderStatus, Photo, PersonStudent, Order, PhotoPersonStudent
from consumers.utils import change_order_status
from shared.logger import logger
from shared.queue import exchange, rabbitmq_broker

MODULE_NAME = 'PHOTOS_PROCESSED'
photos_processed_queue = RabbitQueue('photos_processed')


def init():
    pass


@rabbitmq_broker.handle(photos_processed_queue, exchange, retry=True)
async def photos_processed_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    order_id = message['order_id']
    order = Order.objects.get(id=order_id)
    change_order_status(
        module_name=MODULE_NAME,
        order_id=order_id,
        new_status=OrderStatus.portraits_processed.name
    )
    logger.info(
        module=MODULE_NAME, message='Creation of Photo entities has begun'
    )
    photos_to_create = [
        Photo(
            order=order,
            s3_url=image['s3_url'],
            face_count=image['face_count'],
            focus=image['focus'],
            description=image['description'],
            type=image['type'],
            horizont=image['horizont']
        ) for image in message['images']]
    Photo.objects.bulk_create(photos_to_create)
    logger.info(
        module=MODULE_NAME, message=f'{len(photos_to_create)} entities created'
    )

    logger.info(
        module=MODULE_NAME, message='Creation of PersonStudent entities has begun'
    )
    persons_to_create = []
    photo_person_students_to_create = []
    for person in message['persons']:
        persons_to_create.append(
            PersonStudent(
                vector=person['vector'],
                order=order,
                main_photo=Photo.objects.get(s3_url=person['photos_s3_path'][0])
            )
        )
        for photo_s3_path in person['photos_s3_path']:
            photo_person_students_to_create.append(
                PhotoPersonStudent(
                    photo=Photo.objects.get(s3_url=photo_s3_path),
                    person_student=person,
                )
            )
    PersonStudent.objects.bulk_create(persons_to_create)
    PhotoPersonStudent.objects.bulk_create(photo_person_students_to_create)
    logger.info(
        module=MODULE_NAME, message=f'{len(persons_to_create)} entities created'
    )


async def publish_layouts(data):
    pass
