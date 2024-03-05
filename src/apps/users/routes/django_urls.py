from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.apps.users.views import (
    ListUsersViewSet,
    CustomUserMeViewSet,
    CustomUserViewSet,
)

router = DefaultRouter()


class NoRetriveRouter(DefaultRouter):
    """
    A router that does not return any view for action 'me'
    """

    def get_method_map(self, viewset, method_map):
        """
        Given a viewset, and a mapping of http methods to actions,
        return a new mapping which only includes any mappings that
        are actually implemented by the viewset.

        This router does not return any view for action 'me'
        """

        bound_methods = super().get_method_map(viewset, method_map)

        if (
            "list" in dict(bound_methods).values()
            or "retrieve" in dict(bound_methods).values()
        ):
            del bound_methods["get"]

        return bound_methods


router_for_djoser = NoRetriveRouter()


router_for_djoser.register("auth/users", CustomUserMeViewSet, basename="me")
router.register("users", ListUsersViewSet, basename="users")
router.register("user", CustomUserViewSet, basename="user")


urlpatterns = [
    path("", include(router_for_djoser.urls)),
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
