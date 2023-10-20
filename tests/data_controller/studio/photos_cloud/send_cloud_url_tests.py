from unittest import mock

import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from studio.constants import VALID_DOMAINS
from tests.data_controller.factories import OrderFactory, StudioFactory
from tests.utils import client


class SendCloudUrlTests(APITestCase):

    @pytest.mark.django_db
    @mock.patch('studio.events.PhotosUploadingEvent.handle')
    def test_correct(self, mock_handle):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        order = OrderFactory(studio=studio)
        data = {
            'url': 'https://disk.yandex.ru/d/RTqLhx3YnUxUrQ'
        }
        response = client.post(f'/studio/order/{order.id}/photos/cloud', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'success'})

    @pytest.mark.django_db
    def test_incorrect_domain(self):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        order = OrderFactory(studio=studio)
        data = {
            'url': 'https://disk.neyandex.ru/d/RTqLhx3YnUxUrQ'
        }
        response = client.post(f'/studio/order/{order.id}/photos/cloud', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'url': [f'Необходимо валидный url облака {VALID_DOMAINS}']})

    def test_incorrect_url(self):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        order = OrderFactory(studio=studio)
        data = {
            'url': 'url'
        }
        response = client.post(f'/studio/order/{order.id}/photos/cloud', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'url': ['Enter a valid URL.']})

    @pytest.mark.django_db
    def test_empty_data(self):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        order = OrderFactory(studio=studio)
        response = client.post(f'/studio/order/{order.id}/photos/cloud', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'url': ['This field is required.']})

    @pytest.mark.django_db
    def test_unauthorized(self):
        order = OrderFactory()
        client.force_authenticate(user=None)
        data = {
            'url': 'https://disk.yandex.ru/d/RTqLhx3YnUxUrQ'
        }
        response = client.post(f'/studio/order/{order.id}/photos/cloud', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    @pytest.mark.django_db
    def test_unauthorized_order(self):
        order = OrderFactory()
        client.force_authenticate(user=order.studio)
        another_order = OrderFactory()
        data = {
            'url': 'https://disk.yandex.ru/d/RTqLhx3YnUxUrQ'
        }
        response = client.post(f'/studio/order/{another_order.id}/photos/cloud', data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found.'})
