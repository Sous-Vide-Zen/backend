from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.apps.users.views import (
    ListUsersViewSet,
    CustomUserMeViewSet,
    CustomUserViewSet,
)

router = DefaultRouter()
router.register(r"auth/users", CustomUserMeViewSet, basename="me")
router.register("users", ListUsersViewSet, basename="users")
router.register("user", CustomUserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.jwt")),
]
