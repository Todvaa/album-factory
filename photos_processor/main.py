import asyncio
import json
import os

from dotenv import load_dotenv
from propan import RabbitBroker, PropanApp
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

from classificators import Classificator
from downloaders import MinioDownloader
from recognizers import Recognizer

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
broker = RabbitBroker(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost:{RABBITMQ_PORT}/')
app = PropanApp(broker)
exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)

photos_processing_queue = RabbitQueue('photos_processing')
photos_processed_queue = RabbitQueue('photos_processed')


# todo: добавить логи
@broker.handle(photos_processing_queue, exchange, retry=True)
async def photos_processing_handler(message):
    message = json.loads(message)
    order_id = message['order_id']
    s3_path = message['s3_path']
    local_path = MinioDownloader(order_id=order_id, s3_path=s3_path).run()
    recognizer = Recognizer(dir_path=local_path)
    persons_vectors = recognizer.run()

    classificator = Classificator(vectors=persons_vectors)
    persons = classificator.run()
    # todo: сделать слушателя = консьюмер photo_processing
    # todo: положить в photos_processed


if __name__ == "__main__":
    asyncio.run(app.run())
