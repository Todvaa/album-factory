import asyncio

from propan.brokers.rabbit import RabbitQueue

from shared.queue import exchange, rabbitmq_broker, app

photos_processed_queue = RabbitQueue('photos_processed')


@rabbitmq_broker.handle(photos_processed_queue, exchange, retry=True)
async def photos_processed_handler(message):
    pass


async def publish_layouts(data):
    pass


if __name__ == "__main__":
    asyncio.run(app.run())
