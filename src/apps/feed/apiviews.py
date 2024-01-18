from datetime import datetime, timedelta

from src.apps.recipes.models import Recipe
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets, filters, mixins
from rest_framework.permissions import AllowAny
from .serializers import FeedSerializer
from .pagination import FeedPagination
from django.db.models import Sum, Count, F


class FeedSubscriptionsList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Listing all posts of authors user subscribed to sorted by pub date
    """

    pagination_class = FeedPagination
    serializer_class = FeedSerializer

    def get_queryset(self):
        user = self.request.user
        users_subscribed_to = user.following.all().values_list("user_id", flat=True)
        queryset = (
            Recipe.objects.filter(
                author__in=users_subscribed_to,
                pub_date__gte=datetime.now() - timedelta(days=30),
            )
            .order_by("-pub_date")
            .annotate(
                comments_count=Count("comments"),
                views_count=Count("views"),
                reactions_count=Count("reactions"),
                activity_count=F("comments_count")
                + F("views_count")
                + F("reactions_count"),
            )
        )

        return queryset


class FeedUserList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Listing all created user's posts with pagination and sorting by pub_date
    """

    serializer_class = FeedSerializer
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Recipe.objects.filter(
                author=user,
                pub_date__gte=datetime.now() - timedelta(days=30),
            )
            .order_by("-pub_date")
            .annotate(
                comments_count=Count("comments"),
                views_count=Count("views"),
                reactions_count=Count("reactions"),
                activity_count=F("comments_count")
                + F("views_count")
                + F("reactions_count"),
            )
        )

        return queryset


class FeedPopularList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Listing all popular posts with additional sort by pub_date
    """

    permission_classes = [AllowAny]

    queryset = Recipe.objects.filter(
        pub_date__gte=datetime.now() - timedelta(days=30),
    ).annotate(
        comments_count=Count("comments"),
        views_count=Count("views"),
        reactions_count=Count("reactions"),
        activity_count=F("comments_count") + F("views_count") + F("reactions_count"),
    )
    pagination_class = FeedPagination
    serializer_class = FeedSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["pub_date"]
    ordering = ["-activity_count"]
