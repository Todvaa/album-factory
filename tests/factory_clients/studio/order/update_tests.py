import pytest
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from customer_client.models import Order, OrderStatus
from tests.factory_clients.factories import (
    StudioFactory, OrderFactory, SchoolFactory
)
from tests.utils import client


# data provider
def get_status_cases():
    # Allowed only:
    # While creating => crated
    # Any => rejected
    # layout => agreement

    # init, new, success
    yield OrderStatus.created.name, OrderStatus.portraits_uploading.name, False
    yield OrderStatus.created.name, OrderStatus.portraits_uploaded.name, False
    yield OrderStatus.created.name, OrderStatus.portraits_processing.name, False
    yield OrderStatus.created.name, OrderStatus.portraits_processed.name, False
    yield OrderStatus.created.name, OrderStatus.layout.name, False
    yield OrderStatus.created.name, OrderStatus.agreement.name, False
    yield OrderStatus.created.name, OrderStatus.printing.name, False
    yield OrderStatus.created.name, OrderStatus.completed.name, False
    yield OrderStatus.created.name, OrderStatus.rejected.name, True
    yield OrderStatus.layout.name, OrderStatus.agreement.name, True
    yield OrderStatus.layout.name, OrderStatus.portraits_uploaded.name, False


class UpdateTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        studio = StudioFactory()
        school = SchoolFactory()
        order = OrderFactory()
        order_changed = OrderFactory.build()
        client.force_authenticate(user=order.studio)
        order_params = {
            'class_index': order_changed.class_index,
            'customer_first_name': order_changed.customer_first_name,
            'customer_last_name': order_changed.customer_last_name,
            'customer_middle_name': order_changed.customer_middle_name,
            'phone_number': order_changed.phone_number,
            'albums_count': order_changed.albums_count,
            'passcode': order_changed.passcode,
            'status': OrderStatus.rejected.name,
            'studio': studio.id,
            'school': school.id,
        }
        response = client.patch(f'/studio/order/{order.id}/', data=order_params)
        order_params.update({
            'id': order.id,
            'studio': order.studio.id,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_params, response.data)
        self.assertEqual(Order.objects.count(), 1)
        order_ = Order.objects.get()

        # changed
        self.assertEqual(order_.school.id, school.id)
        self.assertEqual(order_.class_index, order_changed.class_index)
        self.assertEqual(order_.customer_first_name, order_changed.customer_first_name)
        self.assertEqual(order_.customer_last_name, order_changed.customer_last_name)
        self.assertEqual(order_.customer_middle_name, order_changed.customer_middle_name)
        self.assertEqual(order_.phone_number, order_changed.phone_number)
        self.assertEqual(order_.albums_count, order_changed.albums_count)
        self.assertEqual(order_.passcode, order_changed.passcode)
        self.assertEqual(order_.status, OrderStatus.rejected.name)

        # unchanged
        self.assertEqual(order_.studio.id, order.studio.id)

    @pytest.mark.django_db
    def test_unauthorized(self):
        order = OrderFactory()
        client.force_authenticate(user=None)
        response = client.patch(f'/studio/order/{order.id}/', {})
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
        response = client.patch(f'/studio/order/{another_order.id}/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found.'})

    @pytest.mark.django_db
    @parameterized.expand(get_status_cases())
    def test_status(self, init, new, success):
        order = OrderFactory(status=init)
        client.force_authenticate(user=order.studio)
        response = client.patch(f'/studio/order/{order.id}/', {
            'status': new,
        })

        self.assertEqual(Order.objects.get().status, new if success else init)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        )
