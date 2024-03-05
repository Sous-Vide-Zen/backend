from random import sample
from typing import Type

from django.core.exceptions import ValidationError
from django.db.models import Model
from django.utils.translation import gettext_lazy as _


def validate_avatar_size(value):
    if value.size > 5 * 1024 * 1024:  # 5 МБ в байтах
        raise ValidationError(
            _("Размер файла слишком большой. Максимальный размер - 5 МБ.")
        )


def user_avatar_path(instance, filename):
    # При одновременном создании нового пользователя в админке и загрузки аватара,
    # id будет указываться как None

    return f"avatar/user_{instance.id}/{filename}"


def shorten_text(full_text, n) -> str:
    """
    Shorten text to n characters with rounding by last word
    """
    short_text = full_text[:100]
    if len(full_text) > n and full_text[n] != "":
        short_text = short_text[: short_text.rfind(" ")]
    return short_text


def generate_username(user_id: int, model: Type[Model]) -> str:
    """
    Generate a unique username for a user.

    Args:
        user_id (int): The ID of the user.
        model (Type[CustomUser]): The CustomUser model class.

    Returns:
        str: A unique username for the user.
    """

    base_username: str = f"user{user_id}"

    if not model.objects.filter(username=base_username).exists():
        return base_username
    else:

        random_numbers = sample(range(100000, 1000000), 100)
        for random_number in random_numbers:
            new_username = f"user{random_number}"
            if not model.objects.filter(username=new_username).exists():
                return new_username

        return generate_username(user_id, model)
