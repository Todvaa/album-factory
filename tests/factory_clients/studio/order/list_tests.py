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
        response = client.get('/studio/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": order.id,
                    "class_index": order.class_index,
                    "customer_first_name": order.customer_first_name,
                    "customer_last_name": order.customer_last_name,
                    "customer_middle_name": order.customer_middle_name,
                    "phone_number": order.phone_number,
                    "albums_count": order.albums_count,
                    "passcode": order.passcode,
                    "status": order.status,
                    "studio": order.studio.id,
                    "school": order.school.id,
                },
            ]
        }, response.data)

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
