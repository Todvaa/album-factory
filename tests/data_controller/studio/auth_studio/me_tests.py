import pytest
from data_controller.authentication import NAMESPACE_ATTRIBUTE, NAMESPACE_CUSTOMER, NAMESPACE_STUDIO
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from tests.data_controller.factories import StudioFactory, OrderFactory
from tests.utils import client


def check_token(test: APITestCase, token: str):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.get('/studio/auth/me/')
    test.assertEqual(response.status_code, status.HTTP_200_OK)
    client.credentials(HTTP_AUTHORIZATION=None)

    return response


class SigninTests(APITestCase):
    @pytest.mark.django_db
    def test_valid(self):
        studio = StudioFactory()
        refresh = RefreshToken.for_user(studio)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_STUDIO
        token = str(refresh.access_token)
        response = check_token(self, token)
        self.assertEqual(1, response.data['id'])

    @pytest.mark.django_db
    def test_customer_token(self):
        order = OrderFactory()
        refresh = RefreshToken.for_user(order)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_CUSTOMER
        token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/studio/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.django_db
    def test_token_without_namespace(self):
        studio = StudioFactory()
        refresh = RefreshToken.for_user(studio)
        token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/studio/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
