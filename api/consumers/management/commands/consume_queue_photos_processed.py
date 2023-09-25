import asyncio

from django.core.management.base import BaseCommand

from consumers import photos_processed
from shared.queue import app


class Command(BaseCommand):
    help = 'start photos processed consumer'

    def handle(self, *args, **options):
        photos_processed.init()
        asyncio.run(app.run())
