from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_avatar_file(value):
    if not value.name.endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError(_("Неподдерживаемый формат файла. Поддерживаются только .jpg, .jpeg и .png."))


def validate_avatar_size(value):
    if value.size > 5 * 1024 * 1024:  # 5 МБ в байтах
        raise ValidationError(_("Размер файла слишком большой. Максимальный размер - 5 МБ."))


def user_avatar_path(instance, filename):
    # Генерируем путь на основе user_id и расширения файла
    extension = filename.split('.')[-1]
    return f'avatars/{instance.id}/avatar.{extension}'