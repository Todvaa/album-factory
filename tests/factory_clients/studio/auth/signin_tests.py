import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factory_clients.factories import StudioFactory
from tests.utils import client


class SignupTests(APITestCase):
    @pytest.mark.django_db
    def test_valid(self):
        studio = StudioFactory()
        response = client.post('/studio/auth/signin/', {
            'email': studio.email,
            'password': 'password',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)

    @pytest.mark.django_db
    def test_invalid(self):
        studio = StudioFactory()
        response = client.post('/studio/auth/signin/', {
            'email': studio.email,
            'password': 'invalid',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'No active account found with the given credentials'})
