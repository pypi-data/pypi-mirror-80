from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from .views import PermissionViewSet, GroupViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'permissions', PermissionViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Boilerplate API",
        default_version='v1',
        description="Boilerplate API version 1.0.0",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="adminz@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # AUTH 0 authentication
    path('auth0/', include('rest_auth.urls')),

    # OAUTH 2 authentication
    path('auth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Rest Framework API support Browsable API
    path('', include(router.urls)),

    # Rest Framework Auth support Browsable API
    path('', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
]
