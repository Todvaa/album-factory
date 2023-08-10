import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import OrderStatus, Order
from tests.api.factories import OrderFactory
from tests.utils import client


class DetailTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        order = OrderFactory()
        client.force_authenticate(user=order.studio)
        response = client.get(f'/studio/order/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({
            'id': order.id,
            'class_index': order.class_index,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
            'customer_middle_name': order.customer_middle_name,
            'phone_number': order.phone_number,
            'albums_count': order.albums_count,
            'passcode': order.passcode,
            'status': OrderStatus.created.name,
            'school': order.school.id,
            'studio': order.studio.id,
        }, response.data)

    @pytest.mark.django_db
    def test_unauthorized(self):
        order = OrderFactory()
        client.force_authenticate(user=None)
        response = client.get(f'/studio/order/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {'detail': 'Authentication credentials were not provided.'}
        )
        self.assertEqual(Order.objects.count(), 1)

    @pytest.mark.django_db
    def test_unauthorized_order(self):
        order = OrderFactory()
        client.force_authenticate(user=order.studio)
        another_order = OrderFactory()
        response = client.get(f'/studio/order/{another_order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({'detail': 'Not found.'}, response.data)
