# Generated by Django 4.2.6 on 2023-12-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_alter_recipe_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]