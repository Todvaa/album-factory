import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import ConfirmationCode
from tests.utils import client, fake


class ConfirmationTests(APITestCase):
    @pytest.mark.django_db
    def test_reset(self):
        email = fake.email()
        response = client.post('/studio/auth/confirmation_send/', {
            'email': email,
            'action_type': 'reset'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'retryTimeout': 60, 'success': True})
        self.assertEqual(ConfirmationCode.objects.count(), 1)
        self.assertEqual(ConfirmationCode.objects.get().email, email)
        self.assertEqual(ConfirmationCode.objects.get().action_type, 'reset')

    @pytest.mark.django_db
    def test_signup(self):
        email = fake.email()
        response = client.post('/studio/auth/confirmation_send/', {
            'email': email,
            'action_type': 'signup'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'retryTimeout': 60, 'success': True})
        self.assertEqual(ConfirmationCode.objects.count(), 1)
        self.assertEqual(ConfirmationCode.objects.get().email, email)
        self.assertEqual(ConfirmationCode.objects.get().action_type, 'signup')

    @pytest.mark.django_db
    def test_invalid(self):
        response = client.post('/studio/auth/confirmation_send/', {
            'email': '1@invalid',
            'action_type': 'invalid'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'action_type': ['"invalid" is not a valid choice.'],
                                         'email': ['Enter a valid email address.', 'Enter a valid email address.']})
        self.assertEqual(ConfirmationCode.objects.count(), 0)
