from django.db import models

from src.apps.recipes.models import Recipe


class ViewRecipes(models.Model):
    user = models.CharField(max_length=255, db_index=True, verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="views", verbose_name="Рецепт"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время просмотра")

    class Meta:
        verbose_name = "Просмотр рецепта"
        verbose_name_plural = "Просмотры рецептов"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"], name="unique_view")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Пользователь {self.user} просмотрел рецепт {self.recipe}"
