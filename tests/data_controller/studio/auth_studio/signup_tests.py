from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import Studio
from tests.data_controller.factories import ConfirmationCodeFactory, StudioFactory
from tests.utils import fake, client


class SignupTests(APITestCase):
    @pytest.mark.django_db
    def test_valid(self):
        confirmation_code = ConfirmationCodeFactory(action_type='signup')
        response = client.post('/studio/auth/signup/', {
            'email': confirmation_code.email,
            'code': confirmation_code.code,
            'password': fake.password()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(Studio.objects.count(), 1)
        self.assertEqual(Studio.objects.get().email, confirmation_code.email)

    @pytest.mark.django_db
    def test_valid_with_optional(self):
        confirmation_code = ConfirmationCodeFactory(action_type='signup')
        name = fake.name()
        response = client.post('/studio/auth/signup/', {
            'email': confirmation_code.email,
            'code': confirmation_code.code,
            'password': fake.password(),
            'name': name
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(Studio.objects.count(), 1)
        self.assertEqual(Studio.objects.get().email, confirmation_code.email)
        self.assertEqual(Studio.objects.get().name, name)

    @pytest.mark.django_db
    def test_invalid(self):
        response = client.post('/studio/auth/signup/', {
            'email': 'invalid',
            'code': '',
            'password': '',
            'name': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'email': ['Enter a valid email address.', 'Enter a valid email address.'],
                                         'password': ['This field may not be blank.'],
                                         'code': ['This field may not be blank.']})
        self.assertEqual(Studio.objects.count(), 0)

    @pytest.mark.django_db
    def test_existent_email(self):
        studio = StudioFactory()
        confirmation_code = ConfirmationCodeFactory(action_type='signup', email=studio.email)
        response = client.post('/studio/auth/signup/', {
            'email': confirmation_code.email,
            'code': confirmation_code.code,
            'password': fake.password(),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Ошибка при регистрации, почта уже используется'})

    @pytest.mark.django_db
    def test_invalid_code(self):
        confirmation_code = ConfirmationCodeFactory(action_type='signup', code=123456)
        response = client.post('/studio/auth/signup/', {
            'email': confirmation_code.email,
            'code': 654321,
            'password': fake.password()
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'code': ['Неверный код']})
        self.assertEqual(Studio.objects.count(), 0)

    @pytest.mark.django_db
    def test_non_existent_email(self):
        response = client.post('/studio/auth/signup/', {
            'email': Faker().unique.email(),
            'code': 654321,
            'password': fake.password()
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'email': ['Неверно указана почта']})
        self.assertEqual(Studio.objects.count(), 0)

    @pytest.mark.django_db
    def test_outdated_code(self):
        confirmation_code = ConfirmationCodeFactory(
            action_type='signup', date=timezone.make_aware(
                datetime.now() - relativedelta(years=1), timezone.utc
            )
        )
        response = client.post('/studio/auth/signup/', {
            'email': confirmation_code.email,
            'code': confirmation_code.code,
            'password': fake.password()
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'code': ['Срок действия кода истек']})
        self.assertEqual(Studio.objects.count(), 0)
