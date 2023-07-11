from django.core.validators import validate_email
from rest_framework import serializers

from .models import ConfirmationCode, School


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255, required=True, validators=(validate_email, )
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
            raise serializers.ValidationError({'email': ['Неверно указана почта']})
        if confirmation_code.code != code:
            raise serializers.ValidationError({'code': ['Неверный код']})
        if not confirmation_code.valid_code():
            raise serializers.ValidationError({'code': ['Срок действия кода истек']})

        return data


class ConfirmationSendSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255, required=True, validators=(validate_email, )
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
