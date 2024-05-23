from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import (
    PermissionDenied,
    NotAuthenticated,
    ValidationError,
    NotFound,
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.base.code_text import (
    INVALID_ID_FORMAT,
    COMMENT_NOT_FOUND,
    COMMENT_SUCCESSFULLY_DELETE,
    CANT_EDIT_COMMENT,
)
from src.apps.comments.models import Comment
from src.base.paginators import CommentPagination
from src.base.permissions import (
    IsObjectOwnerOrAdminOrReadOnly,
    IsOwnerOrStaffOrReadOnly,
)
from src.base.services import get_or_none
from src.apps.recipes.models import Recipe
from .serializers import CommentListSerializer, CommentCreateSerializer


class CommentViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    """
    Base class for getting, creating, updating and deleting comments
    """

    pagination_class = CommentPagination
    serializer_class = CommentListSerializer

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, slug=self.kwargs.get("slug"))
        queryset = (
            Comment.objects.filter(recipe__slug=recipe.slug)
            .select_related("author")
            .order_by("-updated_date")
        )

        return queryset

    def get_permissions(self):
        permission_classes = {
            "GET": (IsAuthenticatedOrReadOnly,),
            "POST": (IsAuthenticatedOrReadOnly,),
            "PUT": (IsObjectOwnerOrAdminOrReadOnly,),
            "DELETE": (IsOwnerOrStaffOrReadOnly,),
        }
        self.permission_classes = permission_classes.get(self.request.method)

        return super(CommentViewSet, self).get_permissions()

    def get_object(self):
        try:
            user_comments = self.get_queryset().filter(author=self.request.user)
            if not user_comments:
                raise PermissionDenied
        except TypeError:
            raise NotAuthenticated

        try:
            return super().get_object()
        except Exception as error:
            try:
                int(self.kwargs.get("pk"))
            except ValueError:
                raise ValidationError(INVALID_ID_FORMAT, code="invalid_id")
            raise NotFound(COMMENT_NOT_FOUND, code="comment_not_found")

    def get_serializer_class(self):
        if self.request.method == "GET":
            self.serializer_class = CommentListSerializer
        else:
            self.serializer_class = CommentCreateSerializer

        return super(CommentViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        """Creating a comment.
        Comment can be posted on a recipe (indicated by slug in url).

        Comment can be posted on another comment (if "parent" indicated in
        the serializer).
        """

        recipe = get_object_or_404(Recipe, slug=kwargs.get("slug"))
        serializer = self.get_serializer_class()
        serializer = serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        parent = get_or_none(Comment, id=serializer.data["parent"])
        comment = Comment.objects.create(
            author=request.user,
            recipe=recipe,
            parent=parent,
            text=serializer.data["text"],
        )
        serializer = CommentListSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Updating a comment
        """
        comment = self.get_object()
        if timezone.now() - comment.pub_date > timedelta(days=1):
            raise PermissionDenied(CANT_EDIT_COMMENT, code="permission_denied")

        super().update(request, *args, **kwargs)
        comment.refresh_from_db()
        serializer = CommentListSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deleting a comment
        """

        self.get_object().delete()
        return Response(COMMENT_SUCCESSFULLY_DELETE, status=status.HTTP_204_NO_CONTENT)
