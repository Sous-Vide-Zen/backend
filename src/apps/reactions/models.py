from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from .choices import EmojyChoice
from django.contrib.contenttypes.models import ContentType


class Reaction(models.Model):
    """
    Reaction model
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reactions",
        on_delete=models.CASCADE,
    )
    is_deleted = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    emoji = models.CharField(choices=EmojyChoice.choices, max_length=10)
    limit_models = models.Q(app_label="recipes", model="recipe") | models.Q(
        app_label="comments", model="comment"
    )
    content_type = models.ForeignKey(
        ContentType, limit_choices_to=limit_models, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    reaction_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "emoji", "reaction_object"], name="unique_reaction"
            )
        ]
