from django.db import models
from django.conf import settings


class Comment(models.Model):
    """
    Comments model
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
