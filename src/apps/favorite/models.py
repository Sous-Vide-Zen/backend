from django.db import models
from django.conf import settings


class Favorite(models.Model):
    """
    Favorite model
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s favorite recipe: {self.recipe.title}"
