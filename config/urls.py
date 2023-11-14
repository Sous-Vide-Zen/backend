from backend.src.apps.users.views import soc_auth
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("src.apps.api.urls")),
    re_path("", include("social_django.urls", namespace="social")),
    path("soc_auth/", soc_auth),
]
