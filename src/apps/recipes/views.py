from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
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

from config.settings import DRAFTS_MAX_AMOUNT
from src.base.code_text import (
    RECIPE_SUCCESSFUL_DELETE,
    RECIPE_ALREADY_IN_FAVORITES,
    SUCCESSFUL_ADDED_TO_FAVORITES,
    CREDENTIALS_WERE_NOT_PROVIDED,
    THE_RECIPE_IS_NOT_IN_FAVORITES,
    RECIPE_REMOVED_FROM_FAVORITES,
    LIST_OF_FAVORITES_IS_EMPTY,
    AMOUNT_OF_DRAFTS_LESS_THAN_THREE,
    DRAFT_SUCCESSFUL_UPDATE,
)
from src.apps.favorite.models import Favorite
from src.apps.view.models import ViewRecipes
from src.base.paginators import FeedPagination
from src.base.permissions import IsOwnerOrStaffOrReadOnly
from src.base.services import (
    create_draft_slug,
    increment_view_count,
    create_recipe_slug,
    validate_recipe_publishing,
)
from .models import Recipe
from .serializers import (
    RecipeRetrieveSerializer,
    RecipePublicateSerializer,
    RecipeUpdateSerializer,
    BaseRecipeListSerializer,
    DraftSerializer,
)


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
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if "favorites" in self.request.path:
            queryset = (
                Recipe.objects.filter(favorite__author=self.request.user)
                .order_by("-pub_date")
                .prefetch_related("tag", "reactions", "comments", "views")
                .annotate(
                    reactions_count=Count("reactions", distinct=True),
                    views_count=Count("views", distinct=True),
                    comments_count=Count("comments", distinct=True),
                )
            )
            return queryset
        slug = self.kwargs.get("slug")
        queryset = (
            Recipe.objects.filter(slug=slug)
            .select_related("author")
            .prefetch_related("ingredients", "category", "tag", "reactions", "views")
            .annotate(
                reactions_count=Count("reactions", distinct=True),
                views_count=Count("views", distinct=True),
            )
        )

        return queryset

    def get_permissions(self):
        if self.request.method == "POST" or "favorite" or "drafts" in self.request.path:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrStaffOrReadOnly,)

        return super(RecipeViewSet, self).get_permissions()

    def get_serializer_class(self):
        if "publicate" in self.request.path:
            self.serializer_class = RecipePublicateSerializer
        else:
            serializer_classes = {
                "GET": RecipeRetrieveSerializer,
                "POST": DraftSerializer,
                "PATCH": RecipeUpdateSerializer,
            }
            self.serializer_class = serializer_classes.get(self.request.method)

        return super(RecipeViewSet, self).get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        increment_view_count(ViewRecipes, instance, request)

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user_drafts = Recipe.objects.filter(author=request.user, published=False)
        len_user_drafts = len(user_drafts)
        if len_user_drafts >= DRAFTS_MAX_AMOUNT:
            return Response(
                AMOUNT_OF_DRAFTS_LESS_THAN_THREE, status=status.HTTP_400_BAD_REQUEST
            )
        title = f"Черновик"
        slug = create_draft_slug(Recipe, len_user_drafts, request.user.username)

        recipe = Recipe.objects.create(
            author=request.user,
            title=title,
            slug=slug,
            cooking_time=10,
            published=False,
        )
        serializer = DraftSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if recipe.published:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(DRAFT_SUCCESSFUL_UPDATE, status=status.HTTP_200_OK)

    @transaction.atomic
    def publicate_recipe(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data, partial=False)
        validate_recipe_publishing(recipe, serializer)
        if "slug" not in request.data:
            recipe.slug = create_recipe_slug(Recipe, request.data)["slug"]
        recipe.published = True
        recipe.save()
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete recipe"""
        self.get_object().delete()
        return Response(RECIPE_SUCCESSFUL_DELETE, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=[
            "get",
        ],
        pagination_class=FeedPagination,
    )
    def favorites(self, request):
        """Getting a list of favorite user's recipes with pagination."""

        queryset = self.get_queryset()
        if not queryset:
            return Response(LIST_OF_FAVORITES_IS_EMPTY)

        serializer = BaseRecipeListSerializer
        page = self.paginate_queryset(queryset)
        serializer = serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    def add_to_favorites(self, request, slug):
        """Adding a recipe to a list of user's favorites."""
        recipe = get_object_or_404(Recipe, slug=slug)
        favorite_recipe, created = Favorite.objects.get_or_create(
            author=request.user, recipe=recipe
        )
        if not created:
            return Response(
                RECIPE_ALREADY_IN_FAVORITES,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(SUCCESSFUL_ADDED_TO_FAVORITES, status=status.HTTP_201_CREATED)

    def remove_from_favorites(self, request, slug):
        """Removing a recipe from a list of user's favorites."""
        if not request.user.is_authenticated:
            return Response(
                data=CREDENTIALS_WERE_NOT_PROVIDED,
                status=status.HTTP_401_UNAUTHORIZED,
            )
        recipe = get_object_or_404(Recipe, slug=slug)
        favorite_recipe = Favorite.objects.filter(author=request.user, recipe=recipe)

        if not favorite_recipe.exists():
            return Response(
                data=THE_RECIPE_IS_NOT_IN_FAVORITES,
                status=status.HTTP_400_BAD_REQUEST,
            )

        favorite_recipe.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=RECIPE_REMOVED_FROM_FAVORITES,
        )

    def list_draft_recipes(self, request):
        """Getting a list of user's draft recipes."""
        queryset = Recipe.objects.filter(author=request.user, published=False)
        serializer = DraftSerializer(queryset, many=True)

        return Response(serializer.data)
