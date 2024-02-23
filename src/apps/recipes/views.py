from django.db.models import Count
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.view.models import ViewRecipes
from src.base.permissions import IsOwnerOrAdminOrReadOnly
from .models import Recipe
from .serializers import (
    RecipeRetriveSerializer,
    RecipeCreateSerializer,
    RecipeUpdateSerializer,
)
from ...base.services import increment_view_count


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
        if self.request.method == "PATCH":
            self.serializer_class = RecipeUpdateSerializer
        return super(RecipeViewSet, self).get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        increment_view_count(ViewRecipes, instance, request)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
