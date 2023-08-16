import os

from dotenv import load_dotenv
from propan import RabbitBroker, PropanApp
from propan.brokers.rabbit import RabbitExchange, ExchangeType

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)


def get_rabbitmq_broker() -> RabbitBroker:
    return RabbitBroker(
        f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}'
        f'@{RABBITMQ_HOST}:{RABBITMQ_PORT}/'
    )


rabbitmq_broker = get_rabbitmq_broker()
app = PropanApp(rabbitmq_broker)
