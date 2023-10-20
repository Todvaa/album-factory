import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.data_controller.factories import SchoolFactory
from tests.utils import client


class SchoolDetailTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        school = SchoolFactory()
        response = client.get(f'/studio/school/{school.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'id': school.id, 'full_name': school.full_name}
        )

    @pytest.mark.django_db
    def test_not_found(self):
        school = SchoolFactory()
        response = client.get(f'/studio/school/{school.id + 1}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found.'})
