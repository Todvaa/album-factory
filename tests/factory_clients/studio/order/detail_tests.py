import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from customer_client.models import Order
from tests.factory_clients.factories import OrderFactory
from tests.utils import client


class DetailTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        order = OrderFactory()
        client.force_login(order.studio)
        response = client.get('/studio/order/' + order.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({id: 1}, response.data)  # todo: check all fields

    @pytest.mark.django_db
    def test_unauthorized(self):
        order = OrderFactory()
        response = client.get('/studio/order/' + order.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual({'detail': 'error'}, response.data)  # todo: write a normal error
        self.assertEqual(Order.objects.count(), 0)

    @pytest.mark.django_db
    def test_unauthorized_order(self):
        order = OrderFactory()
        client.force_login(order.studio)
        another_order = OrderFactory()
        response = client.get('/studio/order/' + another_order.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual({'detail': 'error'}, response.data)  # todo: write a normal error
