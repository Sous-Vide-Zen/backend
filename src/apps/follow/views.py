from django.db.models import Count
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from src.apps.follow.models import Follow
from src.apps.follow.serializers import FollowListSerializer, FollowerListSerializer
from src.base.paginators import FollowerPagination


class FollowViewSet(GenericViewSet, ListModelMixin):
    serializer_class = FollowListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = FollowerPagination
    swagger_tags = ["subscriptions"]

    def get_queryset(self):
        return (
            Follow.objects.filter(user__username=self.kwargs.get("username"))
            .prefetch_related("user")
            .annotate(subscribers_count=Count("user"))
        )


class FollowerViewSet(GenericViewSet, ListModelMixin):
    serializer_class = FollowerListSerializer
    pagination_class = FollowerPagination
    swagger_tags = ["subscriptions"]

    def get_queryset(self):
        return (
            Follow.objects.filter(author__username=self.kwargs.get("username"))
            .prefetch_related("author")
            .annotate(subscribers_count=Count("user"))
        )
