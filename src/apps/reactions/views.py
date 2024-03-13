from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import GenericViewSet

from src.apps.reactions.models import Reaction
from src.apps.reactions.serializers import (
    RecipeReactionRetriveSerializer,
    RecipeReactionCreateSerializer,
)

from src.apps.recipes.models import Recipe


class RecipeReactionViewSet(
    GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "reactions"
    swagger_tags = ["Reactions"]

    def get_queryset(self):
        queryset = get_list_or_404(Recipe, slug=self.kwargs.get("slug"))
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            self.serializer_class = RecipeReactionRetriveSerializer
        if self.request.method == "POST":
            self.serializer_class = RecipeReactionCreateSerializer
        return super(RecipeReactionViewSet, self).get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a reaction on recipe"""
        recipe = get_object_or_404(Recipe, slug=kwargs.get("slug"))
        content_type = ContentType.objects.get_for_model(recipe)
        serializer = RecipeReactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reaction, created = Reaction.objects.get_or_create(
            emoji=serializer.data["emoji"],
            author=request.user,
            object_id=recipe.id,
            content_type=content_type,
        )

        if not created and not reaction.is_deleted:
            return Response(
                {"detail": "Вы уже поставили такую реакцию к данному рецепту"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if reaction.is_deleted:
            reaction.is_deleted = False
            reaction.save()

        return Response(
            {"message": "Вы оценили рецепт!"}, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        """Delete a reaction on recipe"""
        reaction = get_object_or_404(
            Reaction, id=kwargs.get("pk"), recipe_reactions__slug=kwargs.get("slug")
        )
        if request.user != reaction.author:
            return Response(
                {"detail": "У вас нет разрешения на совершение этого действия."},
                status=status.HTTP_403_FORBIDDEN,
            )
        reaction.is_deleted = True
        reaction.save()
        return Response(
            {"message": "Реакция отменена!"}, status=status.HTTP_204_NO_CONTENT
        )
