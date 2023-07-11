import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factory_clients.factories import SchoolFactory
from tests.utils import client


class SchoolDetailTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        school = SchoolFactory()
        response = client.get('/studio/school/' + str(school.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': school.id, 'name': school.name})

    @pytest.mark.django_db
    def test_default(self):
        school = SchoolFactory()
        response = client.get('/studio/school/' + str(school.id + 1) + '/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     todo: check response.data
