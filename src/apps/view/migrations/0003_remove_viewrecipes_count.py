# Generated by Django 4.2.6 on 2024-01-21 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("view", "0002_viewrecipes_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="viewrecipes",
            name="count",
        ),
    ]