from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings


class Recipe(models.Model):
    """
    Recipe model
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    full_text = models.TextField(max_length=5000, blank=True)
    short_text = models.CharField(max_length=200)
    # ingredient = models.ManyToManyField('Ingredient',related_name='recipes')
    # tag = models.ManyToManyField('Tag',related_name='recipes')
    # category = models.ManyToManyField('Category',related_name='recipes')
    cooking_time = models.PositiveIntegerField(validators=[MaxValueValidator(60 * 24)])
    # views, reactions - foreign keys in Views, Reactions
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        short_text = self.full_text[:100]
        if len(self.full_text) > 100 and self.full_text[100] != "":
            short_text = short_text[: short_text.rfind(" ")]
        self.short_text = short_text
        super().save(*args, **kwargs)
