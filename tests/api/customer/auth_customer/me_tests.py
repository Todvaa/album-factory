import pytest
from api.authentication import NAMESPACE_ATTRIBUTE, NAMESPACE_CUSTOMER, NAMESPACE_STUDIO
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from tests.api.factories import OrderFactory, StudioFactory
from tests.utils import client


def check_token(test: APITestCase, token: str):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.get('/customer/auth/me/')
    test.assertEqual(response.status_code, status.HTTP_200_OK)
    return response


class SigninTests(APITestCase):
    @pytest.mark.django_db
    def test_valid(self):
        order = OrderFactory()
        refresh = RefreshToken.for_user(order)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_CUSTOMER
        token = str(refresh.access_token)
        response = check_token(self, token)
        self.assertEqual(1, response.data['id'])

    @pytest.mark.django_db
    def test_school_token(self):
        studio = StudioFactory()
        refresh = RefreshToken.for_user(studio)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_STUDIO
        token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/customer/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.django_db
    def test_token_without_namespace(self):
        order = OrderFactory()
        refresh = RefreshToken.for_user(order)
        token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/customer/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
