from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('studio/', include('studio.urls', namespace='studio')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('openapi/', get_schema_view(
            title='Album Factory',
            description='External API for studio and customer clients',
            version='dev',
            permission_classes=(AllowAny, ),
        ), name='openapi-schema'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

