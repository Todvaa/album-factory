import asyncio
import json
import os

from propan.brokers.rabbit import RabbitQueue

from classificators import Classificator
from constants import MODULE_NAME
from downloaders import S3Downloader
from dto import Photo
from recognizers import Recognizer
from shared.logger import logger
from shared.queue import rabbitmq_broker, app, exchange, get_rabbitmq_broker
from shared.s3 import ORIGINAL_PH
from shared.s3 import get_photo_url

photos_processing_queue = RabbitQueue('photos_processing')
photos_processed_queue = RabbitQueue('photos_processed')


@rabbitmq_broker.handle(photos_processing_queue, exchange, retry=True)
async def photos_processing_handler(message):
    logger.info(module=MODULE_NAME, message=f'got message: {message}')
    message = json.loads(message)
    order_id = message['order_id']
    s3_path = message['s3_path']
    downloader = S3Downloader(order_id=order_id, s3_path=s3_path)
    local_path = downloader.run()
    photos = [
        Photo(
            name=name, remote_url=get_photo_url(
                order_id=order_id,
                photo_name=name,
                size=ORIGINAL_PH
            )
        ) for name in os.listdir(local_path)
    ]
    recognizer = Recognizer(dir_path=local_path, photos=photos)
    photos_with_vectors = recognizer.run()
    downloader.clean()
    classificator = Classificator(photos=photos_with_vectors)
    persons = classificator.run()
    data = {
        'order_id': order_id,
        'images': [
            {
                's3_url': photo.remote_url,
                'face_count': photo.face_count,
                'focus': photo.focus,
                'description': photo.description,
                'type': photo.type,
                'horizont': photo.horizont,
            } for photo in photos
        ],
        'persons': [
            {
                'photos': person.photo_names,
                'vector': person.average_vector
            } for person in persons
        ]
    }

    await publish_vectors(data=data)
    logger.info(module=MODULE_NAME, message=f'message handled')


async def publish_vectors(data):
    async with get_rabbitmq_broker() as broker:
        logger.info(
            module=MODULE_NAME,
            message=f'pushing message to {photos_processed_queue.name}'
        )
        await broker.publish(
            message=json.dumps(data),
            exchange=exchange, routing_key='photos_processed'
        )
    logger.info(
        module=MODULE_NAME, message=f'pushed'
    )


if __name__ == "__main__":
    asyncio.run(app.run())
