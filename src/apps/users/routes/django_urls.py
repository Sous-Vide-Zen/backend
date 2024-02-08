from src.apps.users.views import CustomUserViewSet, CustomUserMeViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()
router.register(r"auth/users", CustomUserMeViewSet, basename="me")
router.register(r"user", CustomUserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
