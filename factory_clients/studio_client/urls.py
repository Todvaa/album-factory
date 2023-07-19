from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    StudioSignUpView, ConfirmationSendView, SchoolViewSet,
    OrderPhotosCloudView
)

app_name = 'studio_client'

router = DefaultRouter()

router.register(r'school', SchoolViewSet, basename='school')

urlpatterns = [
    path(
        'auth/confirmation_send/',
        ConfirmationSendView.as_view(),
        name='confirmation_send'
    ),
    path('auth/signup/', StudioSignUpView.as_view(), name='sign_up'),
    path('auth/signin/', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'order/<int:order_id>/photos/cloud',
        OrderPhotosCloudView.as_view(),
        name='order_photos_cloud'),
    path('', include(router.urls)),

]
