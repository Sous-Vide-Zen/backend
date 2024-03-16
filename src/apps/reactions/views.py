from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

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

from src.base.throttling import ScopedOnePerThreeSecsThrottle
from src.apps.reactions.models import Reaction
from src.apps.reactions.serializers import (
    RecipeReactionsListSerializer,
    ReactionCreateSerializer,
    CommentReactionsListSerializer,
)

from src.apps.comments.models import Comment
from src.apps.recipes.models import Recipe


class ReactionViewSet(
    GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin
):
    """Base class for getting, creating and deleting reactions."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedOnePerThreeSecsThrottle]
    throttle_scope = "reactions"
    swagger_tags = ["Reactions"]

    def get_queryset(self):
        if "recipe" in self.request.path:
            queryset = Recipe.objects.filter(slug=self.kwargs.get("slug"))

        if "comment" in self.request.path:
            queryset = Comment.objects.filter(id=self.kwargs.get("id"))

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        filter_field = self.kwargs
        obj = get_object_or_404(queryset, **filter_field)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.request.method == "GET":
            if "recipe" in self.request.path:
                self.serializer_class = RecipeReactionsListSerializer
            elif "comment" in self.request.path:
                self.serializer_class = CommentReactionsListSerializer
        if self.request.method == "POST":
            self.serializer_class = ReactionCreateSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        instanse = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(instanse)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        content_type = ContentType.objects.get_for_model(instance)
        serializer = self.get_serializer_class()
        serializer = serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        reaction, created = Reaction.objects.get_or_create(
            emoji=serializer.data["emoji"],
            author=self.request.user,
            object_id=instance.id,
            content_type=content_type,
        )

        if not created and not reaction.is_deleted:
            return Response(
                {"detail": "Вы уже поставили такую реакцию"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if reaction.is_deleted:
            reaction.is_deleted = False
            reaction.save()

        return Response(
            {"message": "Вы поставили оценку!"}, status=status.HTTP_201_CREATED
        )


class RecipeReactionViewSet(ReactionViewSet):
    """Subclass for creating and deleting reactions on recipes"""

    def create(self, request, *args, **kwargs):
        """Create a reaction on recipe"""
        response = super().create(self, request, *args, **kwargs)
        if response.status_code == status.HTTP_403_FORBIDDEN:
            return Response(
                {"detail": "Вы уже поставили такую реакцию к данному рецепту"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {"message": "Вы оценили рецепт!"}, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        reaction = get_object_or_404(
            Reaction,
            id=kwargs.get("pk"),
            recipe_reactions__slug=kwargs.get("slug"),
            author=request.user,
        )

        if request.user != reaction.author:
            return Response(
                {"detail": "У вас недостаточно прав для выполнения данного действия."},
                status=status.HTTP_403_FORBIDDEN,
            )
        reaction.is_deleted = True
        reaction.save()
        return Response(
            {"message": "Реакция отменена!"}, status=status.HTTP_204_NO_CONTENT
        )


class CommentReactionViewSet(ReactionViewSet):
    """Subclass creating and deleting reactions on comment"""

    def create(self, request, *args, **kwargs):
        response = super().create(self, request, *args, **kwargs)
        if response.status_code == status.HTTP_403_FORBIDDEN:
            return Response(
                {"detail": "Вы уже оценили данный комментарий"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {"message": "Вы оценили комментарий!"}, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        reaction = get_object_or_404(
            Reaction,
            id=kwargs.get("pk"),
            comment_reactions__id=kwargs.get("id"),
            author=request.user,
        )
        if request.user != reaction.author:
            return Response(
                {"detail": "У вас недостаточно прав для выполнения данного действия."},
                status=status.HTTP_403_FORBIDDEN,
            )
        reaction.is_deleted = True
        reaction.save()
        return Response(
            {"message": "Реакция отменена!"}, status=status.HTTP_204_NO_CONTENT
        )
