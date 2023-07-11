import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factory_clients.factories import SchoolFactory, StudioFactory
from tests.utils import client


class SchoolCreateTests(APITestCase):
    @pytest.mark.django_db
    def test_valid(self):
        school = SchoolFactory.build()
        client.force_authenticate(user=StudioFactory())
        response = client.post('/studio/school/', {
            'full_name': school.full_name
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, 'full_name': school.full_name})

    @pytest.mark.django_db
    def test_empty_name(self):
        client.force_authenticate(user=StudioFactory())
        response = client.post('/studio/school/', {
            'full_name': ''
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'full_name': ['This field may not be blank.']})

    @pytest.mark.django_db
    def test_none_name(self):
        client.force_authenticate(user=StudioFactory())
        response = client.post('/studio/school/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'full_name': ['This field is required.']})

    @pytest.mark.django_db
    def test_unauthenticated(self):
        client.force_authenticate(user=None)
        response = client.post('/studio/school/', {
            'full_name': 'TEST'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})
