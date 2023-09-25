import asyncio

from django.core.management.base import BaseCommand

from consumers import photos_downloaded
from shared.queue import app


class Command(BaseCommand):
    help = 'start photos downloaded consumer'

    def handle(self, *args, **options):
        photos_downloaded.init()
        asyncio.run(app.run())
