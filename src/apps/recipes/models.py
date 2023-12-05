from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from taggit.managers import TaggableManager

from src.apps.api.services import shorten_text


class Recipe(models.Model):
    """
    Recipe model
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    full_text = models.TextField(max_length=5000, blank=True)
    short_text = models.CharField(max_length=200)
    # ingredient = models.ManyToManyField('Ingredient',related_name='recipes')
    tag = TaggableManager()
    # category = models.ManyToManyField('Category',related_name='recipes')
    cooking_time = models.PositiveIntegerField(validators=[MaxValueValidator(60 * 24)])
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.short_text = shorten_text(self.full_text, 100)
        super().save(*args, **kwargs)
