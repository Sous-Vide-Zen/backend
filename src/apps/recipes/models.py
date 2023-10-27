from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings


class Recipe(models.Model):
    """
    Recipe model
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField()
    full_text = models.TextField(max_length=5000, blank=True)
    short_text = models.CharField()
    ingredient = ""  # TODO: ForeignKey
    tag = ""  # TODO: ForeignKey
    category = ""  # TODO: ForeignKey
    cooking_time = models.PositiveIntegerField(validators=[MaxValueValidator(60 * 24)])
    views = ""  # TODO: ForeignKey
    reactions = ""  # TODO: ForeignKey
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.short_text = self.full_text[:100]  # TODO: round by word?
        super().save(*args, **kwargs)
