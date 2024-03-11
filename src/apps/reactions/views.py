from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ModelViewSet

from src.apps.reactions.models import Reaction
from src.apps.recipes.serializers import (
    RecipeReactionRetriveSerializer,
    RecipeReactionCreateSerializer,
)

from src.apps.recipes.models import Recipe


class RecipeReactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "reactions"

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, slug=self.kwargs.get("slug"))
        queryset = Recipe.objects.filter(id=recipe.id)
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

        if created == False and reaction.is_deleted == False:
            return Response(
                {"detail": "Вы уже поставили такую реакцию к данному рецепту"},
                status=403,
            )
        elif reaction.is_deleted == True:
            reaction.is_deleted = False
            reaction.save()

        return Response({"message": "Вы оценили рецепт!"}, status=201)

    def destroy(self, request, *args, **kwargs):
        """Delete a reaction on recipe"""
        recipe = get_object_or_404(Recipe, slug=kwargs.get("slug"))
        reaction = get_object_or_404(Reaction, id=kwargs.get("pk"), object_id=recipe.id)
        if request.user != reaction.author:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )
        reaction.is_deleted = True
        reaction.save()
        return Response({"message": "Реакция отменена!"}, status=204)
