import os

from dotenv import load_dotenv
from propan import RabbitBroker, PropanApp
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

from classificators import Classificator
from recognizers import Recognizer

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
broker = RabbitBroker(f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost:{RABBITMQ_PORT}/')
app = PropanApp(broker)
exchange = RabbitExchange('album_factory_exchange', type=ExchangeType.DIRECT)

photo_processing_queue = RabbitQueue('photos_processing')
photos_processed_queue = RabbitQueue('photos_processed')


@broker.handle(photo_processing_queue, exchange, retry=True)
def run():
    # local_path = download_photos()
    # recognizer = Recognizer(local_path)
    recognizer = Recognizer('test_photos')
    persons_vectors = recognizer.run()
    classificator = Classificator(persons_vectors)
    persons = classificator.run()
    # todo: сделать слушателя = консьюмер photo_processing
    # todo: положить в photos_processed [persons_vectors, persons]


if __name__ == "__main__":
    run()
