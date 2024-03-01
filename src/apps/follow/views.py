from django.db.models import Count
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from src.apps.follow.models import Follow
from src.apps.follow.serializers import (
    FollowListSerializer,
    FollowerListSerializer,
    FollowCreateSerializer,
)
from src.apps.users.models import CustomUser
from src.base.paginators import FollowerPagination


class FollowViewSet(GenericViewSet, ListModelMixin):
    serializer_class = FollowListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = FollowerPagination
    swagger_tags = ["subscriptions"]

    def get_queryset(self):
        username = self.kwargs.get("username")
        return (
            Follow.objects.filter(user__username=username)
            .select_related("author")
            .annotate(subscribers_count=Count("author__following"))
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        username = kwargs.get("username")
        if not CustomUser.objects.filter(username=username).exists():
            return Response(
                data={"detail": "Пользователь не существует."},
                status=HTTP_404_NOT_FOUND,
            )
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class FollowerViewSet(GenericViewSet, ListModelMixin):
    serializer_class = FollowerListSerializer
    pagination_class = FollowerPagination
    permission_classes = (IsAuthenticated,)
    swagger_tags = ["subscriptions"]

    def get_queryset(self):
        username = self.kwargs.get("username")
        return (
            Follow.objects.filter(author__username=username)
            .select_related("user")
            .annotate(subscribers_count=Count("user__following"))
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        username = kwargs.get("username")
        if not CustomUser.objects.filter(username=username).exists():
            return Response(
                data={"detail": "Пользователь не существует."},
                status=HTTP_404_NOT_FOUND,
            )
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = FollowerListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(ModelViewSet):
    serializer_class = FollowCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ("author__username", "user__username")
    swagger_tags = ["subscriptions"]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        author = request.data.get("author")
        if not author:
            return Response(
                data={"message": "Отсутствует автор"}, status=HTTP_400_BAD_REQUEST
            )

        if not CustomUser.objects.filter(username=request.data.get("author")).exists():
            return Response(
                data={"message": "Автор не найден"}, status=HTTP_404_NOT_FOUND
            )
        super().create(request, *args, **kwargs)

        return Response(
            data={"message": "Вы успешно подписались на автора"},
            status=HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        author = request.data.get("author")
        queryset = Follow.objects.filter(
            user=self.request.user, author__username=author
        )

        if not queryset.exists():
            return Response(
                data={"detail": "Вы не подписаны на этого пользователя."},
                status=HTTP_404_NOT_FOUND,
            )

        queryset.delete()
        return Response(
            data={"message": "Вы успешно отписались от автора"},
            status=HTTP_204_NO_CONTENT,
        )
