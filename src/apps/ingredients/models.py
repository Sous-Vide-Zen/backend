from django.db import models


class Unit(models.Model):
    """
    Unit model
    """

    name = models.CharField(max_length=30)


class Ingredient(models.Model):
    """
    Ingredient model
    """

    name = models.CharField(max_length=100)
    units = models.ManyToManyField(Unit, related_name="ingredients")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
