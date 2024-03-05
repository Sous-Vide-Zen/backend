from django.db.models import Count, Exists, OuterRef
from djoser.views import UserViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from src.apps.follow.models import Follow
from src.base.paginators import UserListPagination
from src.base.permissions import IsOwnerOrAdminOrReadOnly
from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
    CustomUserMeSerializer,
    UserListSerializer,
)


class CustomUserMeViewSet(UserViewSet):
    """
    ViewSet for action 'me'
    """

    swagger_tags = ["CustomUser"]
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        """
        Get serializer class for action 'me'
        """

        if self.action == "me":
            return CustomUserMeSerializer

        return super().get_serializer_class()


class ListUsersViewSet(GenericViewSet, ListModelMixin):
    """
    ViewSet for get all users
    """

    swagger_tags = ["CustomUser"]
    serializer_class = UserListSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = UserListPagination
    lookup_field = "username"

    def get_queryset(self):
        """
        Get all users with recipes_count, is_follow, and is_follower fields.
        """

        user = self.request.user
        queryset = CustomUser.objects.all().annotate(
            recipes_count=Count("recipe"),
        )

        queryset = queryset.annotate(
            is_follow=Exists(Follow.objects.filter(user=user, author=OuterRef("pk"))),
            is_follower=Exists(Follow.objects.filter(author=user, user=OuterRef("pk"))),
        )

        return queryset.order_by("-recipes_count")


class CustomUserViewSet(
    GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
):
    """
    ViewSet for get, update and delete user
    """

    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    swagger_tags = ["CustomUser"]
    lookup_field = "username"
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        """
        Queryset for get, update and delete user
        """

        return CustomUser.objects.filter(username=self.kwargs.get("username"))
