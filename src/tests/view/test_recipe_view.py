from datetime import timedelta

import pytest

from src.apps.view.models import ViewRecipes


@pytest.mark.django_db
class TestRecipeView:
    """
    Test recipe view
    """

    def test_view_recipes(self, api_client, new_recipe, new_author, new_user):
        """
        Test add view for recipe
        """

        assert ViewRecipes.objects.count() == 0
        assert new_recipe.views.count() == 0

        api_client.force_authenticate(user=new_user)
        api_client.get(f"/api/v1/recipe/{new_recipe.slug}/")

        assert ViewRecipes.objects.count() == 1
        assert new_recipe.views.count() == 1

        api_client.force_authenticate(user=new_author)
        api_client.get(f"/api/v1/recipe/{new_recipe.slug}/")

        assert ViewRecipes.objects.count() == 2
        assert new_recipe.views.count() == 2

    def test_view_recipes_one_of_twenty_minutes(self, api_client, new_recipe, new_user):
        """
        Test add view for recipe, one of twenty minutes
        """

        assert new_recipe.views.count() == 0

        api_client.force_authenticate(user=new_user)
        api_client.get(f"/api/v1/recipe/{new_recipe.slug}/")
        assert new_recipe.views.count() == 1
        api_client.get(f"/api/v1/recipe/{new_recipe.slug}/")
        assert new_recipe.views.count() == 1

        # change the first viewing time to 10 minutes
        new_view = ViewRecipes.objects.first()
        new_view.created_at = new_view.created_at - timedelta(minutes=10)
        new_view.save()

        api_client.get(f"/api/v1/recipe/{new_recipe.slug}/")
        assert new_recipe.views.count() == 1

        # change the first viewing time to 20 minutes
        new_view = ViewRecipes.objects.first()
        new_view.created_at = new_view.created_at - timedelta(minutes=10)
        new_view.save()

        api_client.get(f"/api/v1/recipe/{new_recipe.slug}/")
        assert new_recipe.views.count() == 2
