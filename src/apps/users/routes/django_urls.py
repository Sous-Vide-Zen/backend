from src.apps.users.views import CustomUserViewSet, CustomUserMeViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path, re_path

router = DefaultRouter()
router.register(r"auth/users", CustomUserMeViewSet, basename="me")
# router.register(r"users", CustomUserViewSet, basename="user")


# Экземпляры представлений для CustomUserViewSet
user_list_view = CustomUserViewSet.as_view(
    {
        "get": "list",  # GET запросы для списка пользователей
    }
)

user_detail_view = CustomUserViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("users/", user_list_view, name="users-list"),
    re_path(r"^user/(?P<username>[^/.]+)/$", user_detail_view, name="user-detail"),
    path("", include(router.urls)),  # Используйте router без CustomUserViewSetername}/'
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
