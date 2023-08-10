from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.models import Studio, Order


class StudioBackend(BaseBackend):
    def authenticate(self, request, token=None):
        try:
            validated_token = JWTAuthentication.get_validated_token(token)
            studio = validated_token.user
            return studio
        # todo: более конкретный эксепшен
        except:
            return None

    def get_user(self, user_id):
        try:
            return Studio.objects.get(pk=user_id)
        except Studio.DoesNotExist:
            return None


class OrderBackend(BaseBackend):
    def authenticate(self, request, token=None):
        try:
            validated_token = JWTAuthentication.get_validated_token(token)
            order = validated_token.user
            return order
        # todo: более конкретный эксепшен
        except:
            return None

    def get_user(self, user_id):
        try:
            Order.objects.get(pk=user_id)
        except Order.DoesNotExist:
            return None
