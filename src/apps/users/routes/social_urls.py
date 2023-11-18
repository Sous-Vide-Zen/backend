from django.urls import re_path, include

urlpatterns = [
    re_path("", include("social_django.urls", namespace="social")),
]
