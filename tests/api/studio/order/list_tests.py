import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from customer_client.models import Order
from tests.api.factories import OrderFactory, StudioFactory
from tests.utils import client


class ListTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        studio = StudioFactory()
        client.force_login(user=studio)
        OrderFactory.create_batch(50, studio=studio)
        response = client.get('/studio/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 50)
        self.assertEqual(len(response.data['results']), 20)

    @pytest.mark.django_db
    def test_unauthorized(self):
        OrderFactory()
        client.force_authenticate(user=None)
        response = client.get('/studio/order/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {'detail': 'Authentication credentials were not provided.'}
        )
        self.assertEqual(Order.objects.count(), 1)
