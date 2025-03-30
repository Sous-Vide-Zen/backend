from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxLengthValidator
from django.db import models

from src.apps.reactions.models import Reaction
from src.base.code_text import DELETED_RECIPE, DELETED_USER


class Comment(models.Model):
    """
    Comment model

    Attrs:
        • author (ForeignKey): author of a comment.
        • recipe (ForeignKey): recipe, on which a comment was made.
        • text (TextField): text of a comment.
        • pub_date (DateTimeField): comment publication date.
        • parent (ForeignKey): initial comment, on which a comment was made.
        • reactions (GenericRelation): reaction for a comment.
        • updated_date (DateTimeField): comment update date.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        db_index=True,
    )
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.SET_NULL, related_name="comments", null=True
    )
    text = models.TextField(max_length=1000, validators=[MaxLengthValidator(1000)])
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
        db_index=True,
    )
    reactions = GenericRelation(Reaction, related_query_name="comment_reactions")
    updated_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["recipe", "-pub_date"]),
        ]
        ordering = ["-pub_date"]

    def __str__(self):
        """String representation of a comment"""

        author_username = getattr(self.author, "username", DELETED_USER)
        recipe_title = getattr(self.recipe, "title", DELETED_RECIPE)
        return f"{author_username}'s comment on {recipe_title}"
