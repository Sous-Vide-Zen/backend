from django.db.models import Count
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin

from src.apps.follow.models import Follow
from src.apps.follow.serializers import FollowListSerializer
from src.base.paginators import FollowerPagination
from rest_framework.response import Response


class FollowViewSet(GenericViewSet, ListModelMixin):
    serializer_class = FollowListSerializer
    pagination_class = FollowerPagination
    swagger_tags = ["subscriptions"]

    def get_queryset(self):
        return Follow.objects.filter(
            user__username=self.kwargs.get("username")
        ).annotate(subscribers_count=Count("user"))


class FollowerViewSet(GenericViewSet, ListModelMixin):
    serializer_class = FollowListSerializer
    pagination_class = FollowerPagination
    swagger_tags = ["subscriptions"]

    def get_queryset(self):
        return Follow.objects.filter(
            author__username=self.kwargs.get("username")
        ).annotate(subscribers_count=Count("user"))
