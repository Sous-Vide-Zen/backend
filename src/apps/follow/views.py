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
        return Follow.objects.filter(author__username=self.kwargs.get("username")).annotate(subscribers_count=Count('user'))


# class FollowListViewSet(GenericViewSet, ListModelMixin):
#     serializer_class = FollowListSerializer
#     pagination_class = FollowerPagination
#
#     def get_queryset(self):
#         return Follow.objects.filter(author__username=self.kwargs.get("username")).annotate(subscribers_count=Count('user'))
#
#     def list(self, request, *args, **kwargs):
#         return self.list_queryset(self.get_queryset())
#
#     def list_queryset(self, queryset):
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
