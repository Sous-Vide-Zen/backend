from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Count, F, Q, Prefetch
from django.utils.timezone import make_aware
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from src.apps.favorite.models import Favorite
from src.apps.recipes.models import Recipe
from src.base.paginators import FeedPagination
from .filters import FeedFilter
from .serializers import FeedSerializer


class FeedUserList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Listing all posts with sorting by activity_count, filtering by subs and
    username
    """

    pagination_class = FeedPagination
    serializer_class = FeedSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["activity_count"]
    ordering = ["-pub_date"]
    filterset_class = FeedFilter

    def get_queryset(self):
        """
        Get all posts with sorting by activity_count, filtering by subs and
        username
        """

        last_month_start = make_aware(
            datetime.now() - timedelta(days=settings.ACTIVITY_INTERVAL)
        )

        queryset = (
            Recipe.objects.all()
            .only(
                "id",
                "title",
                "slug",
                "category",
                "short_text",
                "preview_image",
                "author_id",
                "author__username",
                "author__display_name",
                "author__avatar",
                "pub_date",
                "tag__name",
                "cooking_time",
            )
            .select_related("author")
            .prefetch_related(
                "tag",
                "category",
                Prefetch(
                    "favorite",
                    queryset=Favorite.objects.filter(
                        author=self.request.user
                        if self.request.user.is_authenticated
                        else None
                    ).select_related("author"),
                    to_attr="user_favorites",
                ),
            )
            .annotate(
                latest_comments_count=Count(
                    "comments",
                    filter=Q(comments__pub_date__gte=last_month_start),
                    distinct=True,
                ),
                latest_views_count=Count(
                    "views",
                    filter=Q(views__created_at__gte=last_month_start),
                    distinct=True,
                ),
                latest_reactions_count=Count(
                    "reactions",
                    filter=Q(reactions__pub_date__gte=last_month_start),
                    distinct=True,
                ),
                comments_count=Count("comments", distinct=True),
                views_count=Count("views", distinct=True),
                reactions_count=Count("reactions", distinct=True),
                activity_count=F("latest_comments_count")
                + F("latest_views_count")
                + F("latest_reactions_count"),
            )
        )
        return queryset

    def get_permissions(self):
        """
        Get permissions for feed list
        """

        subscription = self.request.query_params.get("filter")
        if subscription == "subscriptions":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super(FeedUserList, self).get_permissions()
