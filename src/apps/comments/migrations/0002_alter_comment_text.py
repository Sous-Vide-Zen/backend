# Generated by Django 4.2.6 on 2023-12-28 11:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="text",
            field=models.TextField(
                max_length=1000,
                validators=[django.core.validators.MaxLengthValidator(1000)],
            ),
        ),
    ]