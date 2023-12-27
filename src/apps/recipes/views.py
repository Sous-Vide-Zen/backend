from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing recipes
    """

    queryset = Recipe.objects.all()
    lookup_field = "slug"  # get objects by slug, not pk
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Redefine permissions for delete operation
        """
        if self.request.method in ["DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
