import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.api.factories import OrderFactory
from tests.utils import client
from .me_tests import check_token


class SigninTests(APITestCase):
    @pytest.mark.django_db
    def test_valid(self):
        order = OrderFactory()
        response = client.post('/customer/auth/signin/', {
            'order_id': order.id,
            'passcode': order.passcode,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        token = response.data['access']
        check_token(self, token)
