import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factory_clients.factories import SchoolFactory, StudioFactory
from tests.utils import client


class SchoolDetailTests(APITestCase):
    @pytest.mark.django_db
    def test_valid(self):
        school = SchoolFactory.build()
        client.force_authenticate(user=StudioFactory)
        response = client.post('/studio/school/', {
            'name': school.name
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': school.id, 'name': school.name})

    @pytest.mark.django_db
    def test_empty_name(self):
        client.force_authenticate(user=StudioFactory)
        response = client.post('/studio/school/', {
            'name': ''
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     todo: check response.data

    @pytest.mark.django_db
    def test_none_name(self):
        client.force_authenticate(user=StudioFactory)
        response = client.post('/studio/school/', {
            'name': ''
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     todo: check response.data

    @pytest.mark.django_db
    def test_unauthenticated(self):
        response = client.post('/studio/school/', {
            'name': ''
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     todo: check response.data
