from django.contrib.sessions.backends import file
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_avatar_size(value):
    if value.size > 5 * 1024 * 1024:  # 5 МБ в байтах
        raise ValidationError(
            _("Размер файла слишком большой. Максимальный размер - 5 МБ.")
        )


def user_avatar_path(instance, filename):
    return f"avatar/user_{instance.id}/{file}"
