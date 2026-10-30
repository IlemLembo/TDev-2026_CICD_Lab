from django.urls import path, re_path
from django.conf import settings
from drf_yasg import openapi, generators
from drf_yasg.views import get_schema_view
from rest_framework import permissions

class JWTOAuthSchemaGenerator(generators.OpenAPISchemaGenerator):
    """
    Générateur de schéma personnalisé pour exposer HTTPS et HTTP dynamiquement.
    """
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Inclut à la fois HTTP et HTTPS en dev, ou force selon le contexte
        schema.schemes = ["https", "http"] if settings.DEBUG else ["https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="Description de l'API Blog",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="lemboilem@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=JWTOAuthSchemaGenerator,
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

