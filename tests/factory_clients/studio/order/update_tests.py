import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from customer_client.models import Order, OrderStatus
from tests.factory_clients.factories import StudioFactory, OrderFactory, SchoolFactory
from tests.utils import client


def get_status_cases():
    # Allowed only:
    # Any => completed Maybe rejected later
    # layout => agreement

    # init, new, success
    yield OrderStatus.created.value, OrderStatus.portraits_uploaded.value, False
    yield OrderStatus.created.value, OrderStatus.portraits_processed.value, False
    yield OrderStatus.created.value, OrderStatus.layout.value, False
    yield OrderStatus.created.value, OrderStatus.agreement.value, False
    yield OrderStatus.created.value, OrderStatus.printing.value, False
    yield OrderStatus.created.value, OrderStatus.rejected.value, True
    yield OrderStatus.layout.value, OrderStatus.agreement.value, True
    yield OrderStatus.printing.value, OrderStatus.completed.value, True


class UpdateTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        studio = StudioFactory()
        school = SchoolFactory()
        order = OrderFactory()
        order_changed = OrderFactory.build()
        client.force_login(order.studio)
        response = client.patch('/studio/order/' + order.id, {
            'class_index': order_changed.class_index,
            'customer_first_name': order_changed.customer_first_name,
            'customer_last_name': order_changed.customer_last_name,
            'customer_middle_name': order_changed.customer_middle_name,
            'phone_number': order_changed.phone_number,
            'albums_count': order_changed.albums_count,
            'password': order_changed.password,
            'status': OrderStatus.layout.value,

            'studio': studio.id,
            'school': school.id,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({id: 1}, response.data)  # todo: check all fields
        self.assertEqual(Order.objects.count(), 1)
        # changed
        self.assertEqual(Order.objects.get().school.id, school.id)
        self.assertEqual(Order.objects.get().class_index, order_changed.class_index)
        self.assertEqual(Order.objects.get().customer_first_name, order_changed.customer_first_name)
        self.assertEqual(Order.objects.get().customer_last_name, order_changed.customer_last_name)
        self.assertEqual(Order.objects.get().customer_middle_name, order_changed.customer_middle_name)
        self.assertEqual(Order.objects.get().phone_number, order_changed.phone_number)
        self.assertEqual(Order.objects.get().albums_count, order_changed.albums_count)
        self.assertEqual(Order.objects.get().password, order_changed.password)

        # unchanged
        self.assertEqual(Order.objects.get().studio.id, studio.id)
        self.assertEqual(Order.objects.get().status, OrderStatus.created.value)

    @pytest.mark.django_db
    def test_unauthorized(self):
        order = OrderFactory()
        response = client.patch('/studio/order/' + order.id, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual({'detail': 'error'}, response.data)  # todo: write a normal error
        self.assertEqual(Order.objects.count(), 0)

    @pytest.mark.django_db
    def test_unauthorized_order(self):
        order = OrderFactory()
        client.force_login(order.studio)
        another_order = OrderFactory()
        response = client.patch('/studio/order/' + another_order.id, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual({'detail': 'error'}, response.data)  # todo: write a normal error

    @pytest.mark.django_db
    @pytest.mark.parametrize("init, new, success", get_status_cases())
    def test_status(self, init, new, success):
        order = OrderFactory(status=init)
        client.force_login(order.studio)
        response = client.patch('/studio/order/' + order.id, {
            'status': new,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({id: 1}, response.data)  # todo: check all fields
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().status, new if success else init)
