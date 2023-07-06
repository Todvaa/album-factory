import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmationCode, Studio
from .serializers import ConfirmationSendSerializer, SignUpSerializer
from .utils import generate_random_code

APP_ENV = os.getenv('APP_ENV')


class StudioSignUpView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        name = serializer.validated_data.get('name')
        encrypted_password = make_password(password)
        try:
            studio = Studio.objects.create(
                email=email,
                password=encrypted_password,
                name=name
            )
        except IntegrityError:
            raise ValidationError(
                'Ошибка при регистрации, почта уже используется'
            )

        refresh = RefreshToken.for_user(studio)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)


class ConfirmationSendView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ConfirmationSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        action_type = serializer.validated_data.get('action_type')
        email_code = '000000' if APP_ENV == 'dev' else generate_random_code()
        ConfirmationCode.objects.update_or_create(
            email=email,
            action_type=action_type,
            defaults={
                'code': email_code,
                'date': timezone.now()
            }
        )

        send_mail(
            subject='Album Factory регистрация',
            message=f'Код подтверждения: {email_code}',
            from_email=settings.CONF_EMAIL_TEST,
            recipient_list=[email]
        )

        response_data = {
            'success': True,
            # Для чего это?
            'retryTimeout': 60
        }

        return Response(response_data)
