import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.data_controller.factories import SchoolFactory, StudioFactory
from tests.utils import client


class SchoolListTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        SchoolFactory.create_batch(50, studio=studio)
        response = client.get('/studio/school/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 50)
        self.assertEqual(len(response.data['results']), 20)

    @pytest.mark.django_db
    def test_search(self):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        SchoolFactory.create_batch(50, studio=studio)
        SchoolFactory(full_name='Гимназия 666', studio=studio)
        response = client.get('/studio/school/?search=Гимн')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    @pytest.mark.django_db
    def test_not_found(self):
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        SchoolFactory.create_batch(50, studio=studio)
        response = client.get('/studio/school/?search=Гимн')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

    @pytest.mark.django_db
    def test_foreign_schools(self):
        SchoolFactory.create_batch(50)
        studio = StudioFactory()
        client.force_authenticate(user=studio)
        response = client.get('/studio/school/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)
