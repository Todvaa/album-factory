from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import StudioSignUpView, ConfirmationSendView

app_name = 'studio_client'


urlpatterns = [
    path(
        'auth/confirmation_send/',
        ConfirmationSendView.as_view(),
        name='confirmation_send'
    ),
    path('auth/signup/', StudioSignUpView.as_view(), name='sign_up'),
    path('auth/signin/', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
