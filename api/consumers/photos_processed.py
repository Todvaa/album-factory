import json

from asgiref.sync import sync_to_async
from django.db.models import Q
from propan.brokers.rabbit import RabbitQueue

from common.data_storages import OrderDataStorage
from common.models import OrderStatus, Photo, PersonStudent, Order, PhotoPersonStudent, Template
from shared.logger import logger
from shared.queue import exchange, rabbitmq_broker, get_rabbitmq_broker

MODULE_NAME = 'PHOTOS_PROCESSED'
photos_processed_queue = RabbitQueue('photos_processed')
layouts_generation_queue = RabbitQueue('layouts_generation')


def init():
    pass


def photos_entities_create(order_id: int, images_data: dict):
    logger.info(
        module=MODULE_NAME, message='Creation of Photo entities has begun'
    )
    order = Order.objects.get(id=order_id)
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
        module=MODULE_NAME, message=f'{len(photos_to_create)} entities created'
    )


def person_student_entities_create(order_id: int, persons_data: dict):
    logger.info(
        module=MODULE_NAME, message='Creation of PersonStudent entities has begun'
    )
    order = Order.objects.get(id=order_id)
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
        module=MODULE_NAME, message=f'{len(persons_to_create)} entities created'
    )


def add_templates(message: dict):
    order = Order.objects.get(id=message['order_id'])
    # private_templates = Template.objects.filter(studio=order.studio, public=False)
    # public_templates = Template.objects.filter(public=True)
    # templates = private_templates.union(public_templates)
    query = Q(studio=order.studio, public=False) | Q(public=True)
    templates = Template.objects.filter(query)
    message['templates'] = [template.to_dict() for template in templates]
    logger.info(
        module=MODULE_NAME,
        message=f'templates added'
    )

    return message


def handle(message: dict) -> dict:
    order = Order.objects.get(id=message['order_id'])
    OrderDataStorage.change_status(
        order=order,
        status=OrderStatus.portraits_processed,
        module_name=MODULE_NAME
    )
    photos_entities_create(
        order_id=message['order_id'],
        images_data=message['images']
    )
    person_student_entities_create(
        order_id=message['order_id'],
        persons_data=message['persons']
    )
    message = add_templates(message=message)

    return message


handle_async = sync_to_async(handle)


@rabbitmq_broker.handle(photos_processed_queue, exchange, retry=True)
async def photos_processed_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    await handle_async(
        message=message
    )
    await publish_templates(message=message)
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
