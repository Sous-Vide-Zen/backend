from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet

router = DefaultRouter()
router.register(r"recipe", RecipeViewSet, basename="recipe")

urlpatterns = [
    path(
        "recipe/<slug:slug>/favorite/",
        RecipeViewSet.as_view(
            {"post": "add_to_favorites", "delete": "remove_from_favorites"}
        ),
        name="favorite-recipe",
    ),
    path(
        "recipe/drafts/",
        RecipeViewSet.as_view({"get": "list_draft_recipes"}),
        name="drafts",
    ),
    # path(
    #     "recipe/drafts/<slug:slug>/",
    #     RecipeViewSet.as_view(
    #         {"patch": "update", "get": "retrieve", "delete": "destroy"}
    #     ),
    #     name="drafts",
    # ),
    path(
        "recipe/drafts/<slug:slug>/publicate/",
        RecipeViewSet.as_view({"post": "publicate_recipe"}),
        name="drafts",
    ),
    path("", include(router.urls)),
]
