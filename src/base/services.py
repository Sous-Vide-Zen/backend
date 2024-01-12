from django.core.exceptions import ValidationError
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


def recipe_preview_path(instance, filename):
    return f"preview/recipe_{instance.slug}/{filename}"


def shorten_text(full_text, n) -> str:
    """
    Shorten text to n characters with rounding by last word
    """
    short_text = full_text[:100]
    if len(full_text) > n and full_text[n] != "":
        short_text = short_text[: short_text.rfind(" ")]
    return short_text
