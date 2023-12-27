# Generated by Django 4.2.6 on 2023-12-19 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("follow", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.CheckConstraint(
                check=models.Q(("user", models.F("author")), _negated=True),
                name="same_follower_constraint",
            ),
        ),
    ]