from datetime import datetime, timedelta
from django.db.models import Q
from src.apps.recipes.models import Recipe
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import FeedSerializer
from .pagination import FeedPagination
from django.db.models import Sum, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import FeedFilter


class FeedUserList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Listing all posts with sorting by activity_count, filtering by subs and username
    """

    last_month_start = datetime.now() - timedelta(days=30)
    queryset = Recipe.objects.all().annotate(
        comments_count=Count(
            "comments",
            filter=Q(comments__pub_date__gte=last_month_start),
        ),
        views_count=Count("views", filter=Q(views__created_at__gte=last_month_start)),
        reactions_count=Count(
            "reactions", filter=Q(reactions__pub_date__gte=last_month_start)
        ),
        activity_count=F("comments_count") + F("views_count") + F("reactions_count"),
    )
    pagination_class = FeedPagination
    serializer_class = FeedSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["activity_count"]
    ordering = ["-pub_date"]
    filterset_class = FeedFilter

    def get_permissions(self):
        subscription = self.request.query_params.get("filter")
        if subscription == "subscriptions":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super(FeedUserList, self).get_permissions()
