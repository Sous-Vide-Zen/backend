# Generated by Django 4.2.6 on 2024-02-22 13:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0004_remove_ingredient_units_and_more"),
        ("recipes", "0009_alter_recipe_options_recipe_ingredients_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="category",
            field=models.ManyToManyField(
                blank=True, db_index=True, related_name="recipes", to="recipes.category"
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveIntegerField(
                db_index=True,
                validators=[django.core.validators.MaxValueValidator(1440)],
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                blank=True,
                db_index=True,
                related_name="recipes",
                to="ingredients.ingredientinrecipe",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="pub_date",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterIndexTogether(
            name="category",
            index_together={("name", "slug")},
        ),
    ]
