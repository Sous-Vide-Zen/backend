from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxLengthValidator
from django.db import models

from src.apps.reactions.models import Reaction


class Comment(models.Model):
    """
    Comments model
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
    )
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.SET_NULL, related_name="comments", null=True
    )
    # text = models.TextField(max_length=1000)
    text = models.TextField(max_length=1000, validators=[MaxLengthValidator(1000)])
    pub_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    reactions = GenericRelation(Reaction, related_query_name="comment_reactions")

    def __str__(self):
        return f"{self.author.username} comment to recipe {self.recipe.slug}"
