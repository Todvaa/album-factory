from django.urls import path

from .views import StudioSignInView, MeView

app_name = 'order'

urlpatterns = [
    path('auth/signin/', StudioSignInView.as_view(), name='signin'),
    path('auth/me/', MeView.as_view(), name='me'),
]
