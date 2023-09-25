import json
from typing import List

from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import Q
from propan.brokers.rabbit import RabbitQueue

from common.data_storages import OrderDataStorage
from common.models import OrderStatus, Photo, PersonStudent, Order, PhotoPersonStudent, Template
from shared.logger import logger
from shared.queue import (
    exchange, rabbitmq_broker, get_rabbitmq_broker, RETRY_COUNT
)

MODULE_NAME = 'CONSUMER_PHOTOS_PROCESSED'
photos_processed_queue = RabbitQueue('photos_processed')
layouts_generation_queue = RabbitQueue('layouts_generation')


def init():
    pass


def photos_entities_create(order: Order, images_data: dict):
    logger.info(
        module=MODULE_NAME, message='creation of Photo entities has begun'
    )
    photos_to_create = [
        Photo(
            order=order,
            s3_url=image_data['s3_url'],
            faces_count=image_data['face_count'],
            focus=image_data['focus'],
            description=image_data['description'],
            type=image_data['type'],
            horizont=image_data['horizont']
        ) for image_data in images_data]
    Photo.objects.bulk_create(photos_to_create)
    logger.info(
        module=MODULE_NAME,
        message=f'{len(photos_to_create)} entities added to transaction'
    )


def person_student_entities_create(order: Order, persons_data: dict):
    logger.info(
        module=MODULE_NAME, message='creation of PersonStudent entities has begun'
    )
    persons_to_create = []
    photo_person_students_to_create = []
    for person_data in persons_data:
        person = PersonStudent(
            vector=person_data['vector'],
            order=order,
            main_photo=Photo.objects.get(s3_url=person_data['photos_s3_path'][0])
        )
        persons_to_create.append(person)
        for photo_s3_path in person_data['photos_s3_path']:
            photo_person_students_to_create.append(
                PhotoPersonStudent(
                    photo=Photo.objects.get(s3_url=photo_s3_path),
                    person_student=person,
                )
            )
    PersonStudent.objects.bulk_create(persons_to_create)
    PhotoPersonStudent.objects.bulk_create(photo_person_students_to_create)
    logger.info(
        module=MODULE_NAME,
        message=f'{len(persons_to_create)} entities added to transaction'
    )


def get_templates(order: Order) -> List[dict]:
    query = Q(studio=order.studio, public=False) | Q(public=True)
    templates = Template.objects.filter(query)
    logger.info(
        module=MODULE_NAME,
        message=f'got templates'
    )

    return [template.to_dict() for template in templates]


@transaction.atomic
def handle(message: dict) -> dict:
    try:
        order = Order.objects.get(id=message['order_id'])
    except Order.DoesNotExist as error:
        logger.info(
            module=MODULE_NAME,
            message=f'could not find order by ID. Error{str(error)}'
        )
    OrderDataStorage.change_status(
        order=order,
        status=OrderStatus.portraits_processed,
    )
    photos_entities_create(
        order=order,
        images_data=message['images']
    )
    person_student_entities_create(
        order=order,
        persons_data=message['persons']
    )
    templates = get_templates(order=order)
    message['templates'] = templates

    return message


handle_async = sync_to_async(handle)


@rabbitmq_broker.handle(photos_processed_queue, exchange, retry=RETRY_COUNT)
async def photos_processed_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    message = await handle_async(message)
    logger.info(
        module=MODULE_NAME,
        message='transaction completed'
    )
    await publish_templates(message)
    logger.info(module=MODULE_NAME, message=f'message handled')


async def publish_templates(message):
    async with get_rabbitmq_broker() as broker:
        logger.info(
            module=MODULE_NAME,
            message=f'pushing message to {layouts_generation_queue.name}'
        )
        await broker.publish(
            message=json.dumps(message),
            exchange=exchange, routing_key='layouts_generation'
        )
    logger.info(
        module=MODULE_NAME, message=f'pushed'
    )
