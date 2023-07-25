import asyncio
import os

from dotenv import load_dotenv
from propan import RabbitBroker, PropanApp
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
broker = RabbitBroker(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost:5672/')
app = PropanApp(broker)
exchange = RabbitExchange('upload_photo_exchange', type=ExchangeType.DIRECT)
upload_photo_queue = RabbitQueue('upload_photo')


@broker.handle(upload_photo_queue, exchange)
async def upload_photo_handler(message):
    print(message)


if __name__ == '__main__':
    asyncio.run(app.run())
