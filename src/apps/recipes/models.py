from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models
from taggit.managers import TaggableManager

from src.apps.ingredients.models import IngredientInRecipe
from src.apps.reactions.models import Reaction
from src.base.services import recipe_preview_path, validate_avatar_size


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
    ingredients = models.ManyToManyField(
        IngredientInRecipe, related_name="recipes", blank=True, db_index=True
    )
    tag = TaggableManager(blank=True)
    category = models.ManyToManyField(
        "Category", related_name="recipes", blank=True, db_index=True
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(60 * 24)], db_index=True
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    reactions = GenericRelation(Reaction, related_query_name="reactions")
    is_repost = models.BooleanField(default=False)

    class Meta:
        index_together = ["title", "slug"]
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        """
        String representation
        """
        return f"{self.slug}"


class Category(models.Model):
    """
    Category model
    """

    name = models.CharField(max_length=100, unique=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        index_together = ["name", "slug"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
