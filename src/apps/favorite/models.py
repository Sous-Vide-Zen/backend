from django.db import models
from django.conf import settings


class Favorite(models.Model):
    """
    Favorite model
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)
