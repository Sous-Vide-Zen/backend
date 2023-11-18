from django.db import models
from django.conf import settings


class Favorite(models.Model):
    """
    Favorite model
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
