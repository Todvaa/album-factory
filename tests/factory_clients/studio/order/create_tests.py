import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from customer_client.models import Order, OrderStatus
from tests.factory_clients.factories import StudioFactory, OrderFactory, SchoolFactory
from tests.utils import client


class CreateTests(APITestCase):
    @pytest.mark.django_db
    def test_required(self):
        studio = StudioFactory()
        order = OrderFactory.build()
        client.force_login(studio)
        response = client.put('/studio/order/', {
            'class_index': order.class_index,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({id: 1}, response.data)  # todo: check all fields
        self.assertEqual(Order.objects.count(), 1)

        self.assertEqual(Order.objects.get().studio.id, studio.id)

        self.assertEqual(Order.objects.get().customer_first_name, order.customer_first_name)
        self.assertEqual(Order.objects.get().customer_last_name, order.customer_last_name)
        self.assertEqual(Order.objects.get().class_index, order.class_index)
        self.assertEqual(Order.objects.get().status, OrderStatus.created.value)
        self.assertGreaterEqual(Order.objects.get().password, 100000)

    @pytest.mark.django_db
    def test_optional(self):
        studio = StudioFactory()
        school = SchoolFactory()
        order = OrderFactory.build()
        client.force_login(studio)
        response = client.put('/studio/order/', {
            'class_index': order.class_index,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
            'customer_middle_name': order.customer_middle_name,
            'phone_number': order.phone_number,
            'albums_count': order.albums_count,
            'password': order.password,
            'status': OrderStatus.layout.value,

            'school': school.id,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({id: 1}, response.data)  # todo: check all fields
        self.assertEqual(Order.objects.count(), 1)

        self.assertEqual(Order.objects.get().studio.id, studio.id)
        self.assertEqual(Order.objects.get().school.id, school.id)

        self.assertEqual(Order.objects.get().class_index, order.class_index)
        self.assertEqual(Order.objects.get().customer_first_name, order.customer_first_name)
        self.assertEqual(Order.objects.get().customer_last_name, order.customer_last_name)
        self.assertEqual(Order.objects.get().customer_middle_name, order.customer_middle_name)
        self.assertEqual(Order.objects.get().phone_number, order.phone_number)
        self.assertEqual(Order.objects.get().albums_count, order.albums_count)
        self.assertEqual(Order.objects.get().password, order.password)
        self.assertEqual(Order.objects.get().status, OrderStatus.created.value)
        self.assertGreaterEqual(Order.objects.get().password, 100000)

    @pytest.mark.django_db
    def test_unauthorized(self):
        order = OrderFactory.build()
        response = client.put('/studio/order/', {
            'class_index': order.class_index,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual({'detail': 'error'}, response.data)  # todo: write a normal error
        self.assertEqual(Order.objects.count(), 0)

    @pytest.mark.django_db
    def test_empty(self):
        studio = StudioFactory()
        client.force_login(studio)
        response = client.put('/studio/order/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({'detail': 'error'}, response.data)  # todo: check all fields
        self.assertEqual(Order.objects.count(), 0)
