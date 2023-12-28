from django.db import models


class Unit(models.Model):
    """
    Unit model
    """

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ingredient model
    """

    name = models.CharField(max_length=100, unique=True)
    units = models.ManyToManyField(Unit, related_name="ingredients")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """
    IngredientInRecipe model
    """

    ingredient = models.ForeignKey("Ingredient", null=True, on_delete=models.SET_NULL)
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField()

    def clean_unit(self):
        if self.unit not in self.ingredient.units.all():
            self.ingredient.units.add(self.unit)
            self.ingredient.save()

    def __str__(self):
        return f"{self.recipe.title}_{self.ingredient.name}"
