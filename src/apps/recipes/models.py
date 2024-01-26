from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

from src.apps.reactions.models import Reaction
from src.base.services import recipe_preview_path, shorten_text, validate_avatar_size


class Recipe(models.Model):
    """
    Recipe model
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    full_text = models.TextField()
    short_text = models.CharField(max_length=200)
    preview_image = models.ImageField(
        upload_to=recipe_preview_path,
        blank=True,
        null=True,
        validators=[
            validate_avatar_size,
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
    )
    tag = TaggableManager()
    category = models.ManyToManyField("Category", related_name="recipes", blank=True)
    cooking_time = models.PositiveIntegerField(validators=[MaxValueValidator(60 * 24)])
    pub_date = models.DateTimeField(auto_now_add=True)
    reactions = GenericRelation(Reaction, related_query_name="reactions")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.short_text = shorten_text(self.full_text, 100)
        # check if recipe with such slug already exists

        same_recipes = self.__class__.objects.filter(title=self.title).count()
        slug_str = f"{self.title}_{same_recipes}" if same_recipes else self.title
        self.slug = slugify(slug_str)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"  # name in admin
