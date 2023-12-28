from django.db import models

from src.apps.recipes.models import Recipe


class ViewRecipes(models.Model):
    user = models.CharField(max_length=255, db_index=True, verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="views", verbose_name="Рецепт"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время просмотра")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Просмотр рецепта"
        verbose_name_plural = "Просмотры рецептов"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"], name="unique_view")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Пользователь {self.user} просмотрел рецепт {self.recipe}"

    def increment_view_count(self):
        # Этот метод используется, когда нужно увеличить количество
        # просмотров рецепта в базе данных. Каждый раз, когда происходит
        # просмотр рецепта, этот метод должен быть вызван для соответствующего
        # объекта ViewRecipes, чтобы увеличить и сохранить обновленное количество просмотров.
        # view_recipe.increment_view_count()
        self.count += 1
        self.save()
