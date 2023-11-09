from django.db import models
from django.conf import settings


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
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def delete(self, using=None, keep_parents=False):
        """
        to copy parent of deleted object
        """
        self.parent = self.parent.parent
        self.save()
        super(Comment, self).delete(using=using, keep_parents=keep_parents)
