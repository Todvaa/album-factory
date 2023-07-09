import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factory_clients.factories import SchoolFactory
from tests.utils import client


class ConfirmationTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        SchoolFactory.create_batch(50)
        response = client.get('/studio/school/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.count, 50)
        self.assertEqual(response.data.result.count(), 20)

    @pytest.mark.django_db
    def test_search(self):
        SchoolFactory.create_batch(50)
        SchoolFactory(full_name='Гимназия 666')
        response = client.get('/studio/school?name=гимнАзия/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.count, 1)
        self.assertEqual(response.data.result.count(), 1)

    @pytest.mark.django_db
    def test_not_found(self):
        SchoolFactory.create_batch(50)
        response = client.get('/studio/school?name=гимнАзия/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.count, 0)
        self.assertEqual(response.data.result.count(), 0)
