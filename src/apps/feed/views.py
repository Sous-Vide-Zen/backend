from datetime import datetime, timedelta

from django.db.models import Count, F, Prefetch, Q
from django.utils.timezone import make_aware
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from config.settings import ACTIVITY_INTERVAL
from src.apps.comments.models import Comment
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.view.models import ViewRecipes
from src.base.paginators import FeedPagination
from .filters import FeedFilter
from .serializers import FeedSerializer


class FeedUserList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Listing all posts with sorting by activity_count, filtering by subs and username
    """

    pagination_class = FeedPagination
    serializer_class = FeedSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["activity_count"]
    ordering = ["-pub_date"]
    filterset_class = FeedFilter

    def get_queryset(self):
        last_month_start = make_aware(
            datetime.now() - timedelta(days=ACTIVITY_INTERVAL)
        )
        queryset = (
            Recipe.objects.all()
            .prefetch_related(
                Prefetch(
                    "comments",
                    queryset=Comment.objects.all(),
                ),
                Prefetch(
                    "views",
                    queryset=ViewRecipes.objects.all(),
                ),
                Prefetch(
                    "reactions",
                    queryset=Reaction.objects.all(),
                ),
            )
            .annotate(
                comments_count=Count(
                    "comments", filter=Q(comments__pub_date__gte=last_month_start)
                ),
                views_count=Count(
                    "views",
                    filter=Q(views__created_at__gte=last_month_start),
                ),
                reactions_count=Count(
                    "reactions",
                    filter=Q(reactions__pub_date__gte=last_month_start),
                ),
                total_comments_count=Count("comments"),
                total_views_count=Count("views"),
                total_reactions_count=Count("reactions"),
                activity_count=F("comments_count")
                + F("views_count")
                + F("reactions_count"),
            )
        )
        return queryset

    def get_permissions(self):
        subscription = self.request.query_params.get("filter")
        if subscription == "subscriptions":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super(FeedUserList, self).get_permissions()
