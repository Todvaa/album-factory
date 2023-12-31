import os

from aiormq import AMQPConnectionError
from data_controller.authentication import NAMESPACE_ATTRIBUTE, NAMESPACE_STUDIO
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import ConfirmationCode, Studio, School, OrderStatus, Order
from .events import PhotosUploadingEvent
from .mixins import CreateRetrieveListViewSet, CreateRetrieveListUpdateViewSet
from .permissions import IsOwner
from .serializers import (
    ConfirmationSendSerializer, SignUpSerializer, SchoolSerializer,
    OrderSerializer, OrderPhotosCloudSerializer, StudioSerializer, SignInSerializer
)
from .utils import generate_random_code

APP_ENV = os.getenv('APP_ENV')


class StudioSignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

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
            raise ValidationError({
                'error': 'Ошибка при регистрации, почта уже используется'
            })

        refresh = RefreshToken.for_user(studio)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_STUDIO
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)


class StudioTokenObtainPairView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            studio = Studio.objects.get(
                email=email,
            )
        except Studio.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        if not check_password(password, studio.password):
            raise AuthenticationFailed('User not found', code='user_not_found')

        refresh = RefreshToken.for_user(studio)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_STUDIO
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)


class MeView(GenericAPIView):
    serializer_class = StudioSerializer

    def get(self, request):
        return Response(self.serializer_class(request.user).data)


class ConfirmationSendView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmationSendSerializer

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
            # todo: потом надо сделать проверку что если код отправлен менее retryTimeout, то повторный код не
            #  отправляем и соответственно выводим время сколько осталось до нового кода
            'retryTimeout': 60
        }

        return Response(response_data)


class OrderPhotosCloudView(GenericAPIView):
    serializer_class = OrderPhotosCloudSerializer

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, studio=request.user)
        serializer = OrderPhotosCloudSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            PhotosUploadingEvent(url=serializer.validated_data['url'], order_id=order_id).handle()
            order.status = OrderStatus.portraits_uploading.name
            order.save()

        except AMQPConnectionError:
            return Response({'detail': 'Retry later'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response({'detail': 'success'})


class SchoolViewSet(CreateRetrieveListViewSet):
    serializer_class = SchoolSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('full_name',)

    def perform_create(self, serializer):
        serializer.save(studio=self.request.user)

    def get_queryset(self):
        return School.objects.filter(studio=self.request.user)


class OrderViewSet(CreateRetrieveListUpdateViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsOwner & IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(studio=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(studio=self.request.user)
