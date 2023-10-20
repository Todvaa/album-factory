import unittest

import pytest

from consumers.photos_processed import get_templates
from tests.data_controller.factories import StudioFactory, TemplateFactory, OrderFactory


class PhotoProcessedTest(unittest.TestCase):
    @pytest.mark.django_db
    def test_get_templates(self):
        studio = StudioFactory()
        order = OrderFactory(studio=studio)
        other_studio = StudioFactory()
        # must find
        TemplateFactory(public=True)
        TemplateFactory.create_batch(2, studio=other_studio, public=True)
        TemplateFactory.create_batch(4, studio=studio, public=True)
        TemplateFactory.create_batch(8, studio=studio)
        # must not find
        TemplateFactory.create_batch(16, studio=other_studio)

        templates = get_templates(order=order)
        self.assertEqual(len(templates), 15)
