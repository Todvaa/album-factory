import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factory_clients.factories import SchoolFactory
from tests.utils import client


class SchoolListTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        SchoolFactory.create_batch(50)
        response = client.get('/studio/school/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 50)

    @pytest.mark.django_db
    def test_search(self):
        SchoolFactory(full_name='Гимназия 666')
        response = client.get('/studio/school/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @pytest.mark.django_db
    def test_not_found(self):
        SchoolFactory.create_batch(50)
        response = client.get('/studio/school/?search=гимнАзия/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
