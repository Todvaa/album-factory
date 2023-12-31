from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudioSignUpView, ConfirmationSendView, SchoolViewSet, OrderViewSet,
    OrderPhotosCloudView, MeView, StudioTokenObtainPairView,
)

app_name = 'studio'

router = DefaultRouter()

router.register(r'school', SchoolViewSet, basename='school')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path(
        'auth/confirmation_send/',
        ConfirmationSendView.as_view(),
        name='confirmation_send'
    ),
    path('auth/signup/', StudioSignUpView.as_view(), name='sign_up'),
    path('auth/signin/', StudioTokenObtainPairView.as_view(), name='get_token'),
    # path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
    path(
        'order/<int:order_id>/photos/cloud',
        OrderPhotosCloudView.as_view(),
        name='order_photos_cloud'),
    path('', include(router.urls)),
]
