# Generated by Django 4.2.6 on 2024-03-09 08:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_customuser_username"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "ordering": ["-date_joined"],
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
        migrations.AlterModelManagers(
            name="customuser",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="join_date",
        ),
        migrations.AddField(
            model_name="customuser",
            name="display_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="city",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=30,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Zа-яА-Я\\s\\-\\‘\\u00C0-\\u017F]+$"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="country",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=30,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Zа-яА-Я\\s\\-\\‘\\u00C0-\\u017F]+$"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=30,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Zа-яА-Я\\s\\-\\‘\\u00C0-\\u017F]+$"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=30,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Zа-яА-Я\\s\\-\\‘\\u00C0-\\u017F]+$"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]