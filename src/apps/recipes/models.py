from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from taggit.managers import TaggableManager

from src.apps.ingredients.models import IngredientInRecipe
from src.apps.reactions.models import Reaction
from src.base.services import recipe_preview_path, validate_avatar_size
from src.base.code_text import VALIDATE_REPOST_OWN_POST


class Recipe(models.Model):
    """
    Recipe model

    Attrs:
    • author (ForeignKey): author of recipe.
    • title (CharField(150)): title of recipe.
    • slug (SlugField): slug of recipe.
    • full_text (TextField): recipe's full text.
    • short_text (CharField(200)): recipe's short text.
    • preview_image (ImageField): preview image of ready-made dish.
    • ingredients (ManyToManyField): ingredients of recipe.
    • tag (TaggableManager): tag of recipe.
    • category (ManyToManyField): category of recipe.
    • cooking_time (PositiveIntegerField): time of cooking.
    • pub_date (DateTimeField): recipe publication date.
    • updated_at (DateTimeField): recipe updated date.
    • reactions (GenericRelation): reactions on a recipe.
    • is_repost (BooleanField): indicates whether recipe was reposted. Default False.
    • published (BooleanField): indicates whether recipe was published or it's a draft (if False).
    • original_recipe (ForeignKey): original recipe.

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
        IngredientInRecipe, related_name="recipes", blank=True
    )
    tag = TaggableManager(blank=True)
    category = models.ManyToManyField("Category", related_name="recipes", blank=True)
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(60 * 24),
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    reactions = GenericRelation(Reaction, related_query_name="recipe_reactions")
    is_repost = models.BooleanField(default=False)
    published = models.BooleanField(default=False, db_index=True)
    original_recipe = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reposts",
        db_index=True,
    )

    class Meta:
        """
        Meta

        Attrs:
        • indexes (list): indexes of recipe model.
        • verbose_name (str): verbose name of recipe model.
        • verbose_name_plural (str): verbose name of recipe model.
        """

        indexes = [
            models.Index(fields=["title", "slug"]),
            models.Index(fields=["published", "pub_date"]),
        ]
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def clean(self):
        """
        Clean method

        Raises:
        • ValidationError: if recipe was reposted by the author.
        """

        super().clean()
        if (
            self.is_repost
            and self.original_recipe
            and self.original_recipe.author == self.author
        ):
            raise ValidationError(VALIDATE_REPOST_OWN_POST)

    def __str__(self):
        """
        String representation
        """

        return f"{self.slug}"


class Category(models.Model):
    """
    Category model

    Attrs:
    • name (CharField(100)): name of category.
    • slug (SlugField): slug of category.
    """

    name = models.CharField(max_length=100, unique=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        index_together = ["name", "slug"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
