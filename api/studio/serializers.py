from urllib.parse import urlparse

from api.authentication import NAMESPACE_ATTRIBUTE, NAMESPACE_STUDIO
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import ConfirmationCode, School, OrderStatus, Order, Studio
from .constants import VALID_DOMAINS


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255, required=True, validators=(validate_email,)
    )
    password = serializers.CharField(max_length=150, required=True)
    code = serializers.CharField(max_length=10, required=True)
    name = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        try:
            confirmation_code = ConfirmationCode.objects.get(
                email=email,
                action_type='signup'
            )
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError(
                {'email': ['Неверно указана почта']}
            )
        if confirmation_code.code != code:
            raise serializers.ValidationError(
                {'code': ['Неверный код']}
            )
        if not confirmation_code.valid_code():
            raise serializers.ValidationError(
                {'code': ['Срок действия кода истек']}
            )

        return data


class StudioTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        refresh = RefreshToken.for_user(user)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_STUDIO

        return refresh


class OrderPhotosCloudSerializer(serializers.Serializer):
    url = serializers.URLField()

    def validate(self, data):
        url = urlparse(data.get('url'))
        hostname = url.hostname
        domain = hostname.split('.')[-2]
        if domain not in VALID_DOMAINS:
            raise serializers.ValidationError(
                {'url': [f'Необходимо валидный url облака {VALID_DOMAINS}']}
            )

        return data


class ConfirmationSendSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255, required=True, validators=(validate_email,)
    )
    action_type = serializers.ChoiceField(
        choices=('signup', 'reset'), required=True
    )


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            'id', 'full_name',
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'class_index', 'customer_first_name', 'customer_last_name',
            'customer_middle_name', 'phone_number', 'albums_count',
            'passcode', 'status', 'studio', 'school'
        )
        read_only_fields = (
            'studio',
        )

    def validate_status(self, value):
        if self.instance is None:
            raise serializers.ValidationError(['Недопустимое изменение статуса'])

        current_status = self.instance.status
        match value:
            case OrderStatus.rejected.name:
                return value
            case OrderStatus.agreement.name if (
                    current_status == OrderStatus.layout.name
            ):
                return value
            case _:
                raise serializers.ValidationError(['Недопустимое изменение статуса'])


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = (
            'id', 'email', 'name',
        )
        read_only_fields = (
            'id', 'email', 'name',
        )
