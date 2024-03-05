from django.db.models import Count, Exists, OuterRef
from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.follow.models import Follow
from src.base.paginators import UserListPagination
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

    @swagger_auto_schema(methods=["get"], responses={200: CustomUserMeSerializer})
    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "me":
            return CustomUserMeSerializer
        return super().get_serializer_class()

    def get_object(self):
        # Возвращает объект текущего пользователя для действия 'me'
        if self.action == "me":
            return self.request.user
        return super().get_object()

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        if getattr(self, "current_action", None) == "me":
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)


class CustomUserViewSet(
    GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
):
    swagger_tags = ["CustomUser"]
    lookup_field = "username"
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "patch", "delete"]
