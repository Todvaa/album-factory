import unittest

import pytest

from consumers.photos_processed import get_templates
from tests.api.factories import StudioFactory, TemplateFactory, OrderFactory


class PhotoProcessedTest(unittest.TestCase):
    @pytest.mark.django_db
    def test_get_templates(self):
        studio = StudioFactory()
        order = OrderFactory(studio=studio)
        other_studio = StudioFactory()
        TemplateFactory.create_batch(10)
        TemplateFactory.create_batch(5, studio=other_studio)
        TemplateFactory.create_batch(5, studio=other_studio, public=False)
        TemplateFactory.create_batch(5, studio=studio)
        TemplateFactory.create_batch(5, studio=studio, public=False)
        templates = get_templates(order=order)
        self.assertEqual(len(templates), 25)
