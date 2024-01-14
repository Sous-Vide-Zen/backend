from src.apps.recipes.models import Recipe
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets, filters
from .serializers import FeedSerializer
from django.db.models import Sum, Count, F


class FeedPopularPagination(PageNumberPagination):
    page_size = 5


class FeedPopularList(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Listing all popular posts with additional sort by pub_date
    """

    queryset = Recipe.objects.annotate(
        comments_count=Count("comments"),
        views_count=Count("views"),
        reactions_count=Count("reactions"),
        activity_count=F("comments_count") + F("views_count") + F("reactions_count"),
    )
    pagination_class = FeedPopularPagination
    serializer_class = FeedSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["pub_date"]
    ordering = ["-activity_count"]
