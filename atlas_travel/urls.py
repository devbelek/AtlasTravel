from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Документация",
        default_version='v1',
        description="Detailed description of API endpoints",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/', include('tours.urls')),
    path('api/', include('flights.urls')),
    path('api/', include('hotels.urls')),
    path('api/', include('transfer.urls')),
    path('api/', include('about.urls')),
    path('api/', include('common.urls')),
    path('api/', include('contacts.urls')),
    path('api/', include('main.urls')),
    path('api/', include('blog.urls')),
    path('api/', include('services.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)