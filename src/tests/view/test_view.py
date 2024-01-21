import pytest
from django.db.utils import IntegrityError

from src.apps.view.models import ViewRecipes


@pytest.mark.django_db
class TestViewRecipesModel:
    def test_initial_view_count(self, new_user, new_recipe):
        # Проверка начального значения count при создании новой записи
        view = ViewRecipes.objects.create(user=new_user.username, recipe=new_recipe)
        assert view.count == 0

    def test_view_recipe_uniqueness(self, new_user, new_recipe):
        # Создание записи о просмотре и попытка создать дублирующую запись
        ViewRecipes.objects.create(user=new_user.username, recipe=new_recipe)
        with pytest.raises(IntegrityError):
            ViewRecipes.objects.create(user=new_user.username, recipe=new_recipe)
