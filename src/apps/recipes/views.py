from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from config.settings import TIME_FROM_VIEW_RECIPE
from src.base.permissions import IsOwnerOrAdminOrReadOnly
from .models import Recipe
from .serializers import RecipeRetriveSerializer, RecipeCreateSerializer
from ..view.models import ViewRecipes


class RecipeViewSet(
    GenericViewSet,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    filter_backends = (SearchFilter,)
    search_fields = ("title",)
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        queryset = (
            Recipe.objects.filter(slug=slug)
            .select_related("author")
            .prefetch_related(
                "ingredients",
                "category",
                "tag",
                "reactions",
            )
            .annotate(
                reactions_count=Count("reactions", distinct=True),
                views_count=Count("views", distinct=True),
            )
        )
        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = (AllowAny,)
        if self.request.method == "POST":
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrAdminOrReadOnly,)
        return super(RecipeViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            self.serializer_class = RecipeRetriveSerializer
        if self.request.method == "POST":
            self.serializer_class = RecipeCreateSerializer
        return super(RecipeViewSet, self).get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.increment_view_count(instance, request)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def increment_view_count(self, recipe, request):
        user_id = request.user.id if request.user.is_authenticated else "anonymous"
        time_threshold = timezone.now() - timedelta(minutes=TIME_FROM_VIEW_RECIPE)

        view_exists = ViewRecipes.objects.filter(
            user=user_id, recipe=recipe, created_at__gte=time_threshold
        ).exists()
        print("view_exists=", view_exists)

        if not view_exists:
            print("create view")
            ViewRecipes.objects.create(user=user_id, recipe=recipe)
