import pytest
from src.apps.view.models import ViewRecipes
from django.db.utils import IntegrityError


@pytest.mark.django_db
class TestViewRecipesModel:
    def test_increment_view_count(self, new_user, new_recipe):
        # Создание записи о просмотре и проверка начального значения count
        view = ViewRecipes.objects.create(user=new_user.username, recipe=new_recipe)
        assert view.count == 0

        # Инкрементирование count и сохранение
        view.count += 1
        view.save()

        # Получение записи из базы данных и проверка обновленного значения count
        updated_view = ViewRecipes.objects.get(id=view.id)
        assert updated_view.count == 1

    def test_initial_view_count(self, new_user, new_recipe):
        # Проверка начального значения count при создании новой записи
        view = ViewRecipes.objects.create(user=new_user.username, recipe=new_recipe)
        assert view.count == 0

    def test_view_recipe_uniqueness(self, new_user, new_recipe):
        # Создание записи о просмотре и попытка создать дублирующую запись
        ViewRecipes.objects.create(user=new_user.username, recipe=new_recipe)
        with pytest.raises(IntegrityError):
            ViewRecipes.objects.create(user=new_user.username, recipe=new_recipe)
