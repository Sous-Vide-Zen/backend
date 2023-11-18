from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Sous VIDE ZEN API",
        default_version="v1",
        description="Документация для проекта SOUS VIDE ZEN",
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    authentication_classes=[JWTAuthentication],
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", RedirectView.as_view(url="swagger/", permanent=False), name="index"),
]
