from django.urls import path

from .views import CustomerSignInView, MeView

app_name = 'customer'

urlpatterns = [
    path('auth/signin/', CustomerSignInView.as_view(), name='signin'),
    path('auth/me/', MeView.as_view(), name='me'),
]
