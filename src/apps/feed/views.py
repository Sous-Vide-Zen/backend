from datetime import datetime, timedelta

from django.db.models import Count, F, Prefetch, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from config.settings import ACTIVITY_INTERVAL
from src.apps.comments.models import Comment
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.view.models import ViewRecipes
from .filters import FeedFilter
from .pagination import FeedPagination
from .serializers import FeedSerializer
from django.utils.timezone import make_aware


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
                    queryset=Comment.objects.filter(pub_date__gte=last_month_start),
                ),
                Prefetch(
                    "views",
                    queryset=ViewRecipes.objects.filter(
                        created_at__gte=last_month_start
                    ),
                ),
                Prefetch(
                    "reactions",
                    queryset=Reaction.objects.filter(pub_date__gte=last_month_start),
                ),
            )
            .annotate(
                comments_count=Coalesce(
                    Subquery(
                        Comment.objects.filter(
                            recipe=OuterRef("pk"), pub_date__gte=last_month_start
                        )
                        .values("recipe")
                        .annotate(count=Count("pk"))
                        .values("count")
                    ),
                    0,
                ),
                views_count=Coalesce(
                    Subquery(
                        ViewRecipes.objects.filter(
                            recipe=OuterRef("pk"), created_at__gte=last_month_start
                        )
                        .values("recipe")
                        .annotate(count=Count("pk"))
                        .values("count")
                    ),
                    0,
                ),
                reactions_count=Coalesce(
                    Subquery(
                        Reaction.objects.filter(
                            object_id=OuterRef("pk"), pub_date__gte=last_month_start
                        )
                        .values("object_id")
                        .annotate(count=Count("pk"))
                        .values("count")
                    ),
                    0,
                ),
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
