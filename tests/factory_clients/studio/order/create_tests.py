import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from customer_client.models import Order, OrderStatus
from tests.factory_clients.factories import (
    StudioFactory, OrderFactory, SchoolFactory
)
from tests.utils import client


class CreateTests(APITestCase):
    @pytest.mark.django_db
    def test_required(self):
        studio = StudioFactory()
        order = OrderFactory.build()
        client.force_authenticate(user=studio)
        order_params = {
            'class_index': order.class_index,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
            'albums_count': order.albums_count
        }
        response = client.post('/studio/order/', data=order_params)
        order_params.update({
            'id': 1,
            'customer_middle_name': None,
            'passcode': response.data['passcode'],
            'phone_number': None,
            'school': None,
            'status': OrderStatus.created.value,
            'studio': studio.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order_params, response.data)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.studio.id, studio.id)
        self.assertEqual(order.customer_first_name, order.customer_first_name)
        self.assertEqual(order.customer_last_name, order.customer_last_name)
        self.assertEqual(order.class_index, order.class_index)
        self.assertEqual(order.status, OrderStatus.created.value)
        self.assertGreaterEqual(order.passcode, 100000)

    @pytest.mark.django_db
    def test_optional(self):
        studio = StudioFactory()
        school = SchoolFactory()
        order = OrderFactory.build()
        order_params = {
            'class_index': order.class_index,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
            'customer_middle_name': order.customer_middle_name,
            'phone_number': order.phone_number,
            'albums_count': order.albums_count,
            'passcode': order.passcode,
            'status': OrderStatus.rejected.value,
            'school': school.id,
        }
        client.force_authenticate(user=studio)
        response = client.post('/studio/order/', data=order_params)
        order_params.update({
            'id': 1,
            'passcode': response.data['passcode'],
            'studio': studio.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order_params, response.data)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.studio.id, studio.id)
        self.assertEqual(order.school.id, school.id)
        self.assertEqual(order.class_index, order.class_index)
        self.assertEqual(order.customer_first_name, order.customer_first_name)
        self.assertEqual(order.customer_last_name, order.customer_last_name)
        self.assertEqual(order.customer_middle_name, order.customer_middle_name)
        self.assertEqual(order.phone_number, order.phone_number)
        self.assertEqual(order.albums_count, order.albums_count)
        self.assertEqual(order.passcode, order.passcode)
        self.assertEqual(order.status, OrderStatus.rejected.value)
        self.assertGreaterEqual(order.passcode, 100000)

    @pytest.mark.django_db
    def test_unauthorized(self):
        order = OrderFactory.build()
        client.force_authenticate(user=None)
        response = client.post('/studio/order/', {
            'class_index': order.class_index,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
            'albums_count': order.albums_count,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {'detail': 'Authentication credentials were not provided.'}
        )
        self.assertEqual(Order.objects.count(), 0)

    @pytest.mark.django_db
    def test_empty(self):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        response = client.post('/studio/order/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "class_index": ["This field is required."],
            "customer_first_name": ["This field is required."],
            "customer_last_name": ["This field is required."],
            "albums_count": ["This field is required."]})
        self.assertEqual(Order.objects.count(), 0)
