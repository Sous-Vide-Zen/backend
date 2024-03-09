from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Пароль должен состоять не менее чем из 8 символов."),
                code="password_too_short",
            )
        if not re.findall("[a-z]", password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну строчную букву (a-z)."),
                code="password_no_lower",
            )
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну заглавную букву (A-Z)."),
                code="password_no_upper",
            )
        if not re.findall("[0-9]", password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну цифру (0-9)."),
                code="password_no_number",
            )
        if not re.findall("[!@#$%^&*]", password):
            raise ValidationError(
                _(
                    "Пароль должен содержать хотя бы один специальный символ (!@#$%^&*)."
                ),
                code="password_no_special",
            )

    def get_help_text(self):
        return _(
            "Пароль должен состоять не менее чем из 8 символов:"
            " минимум с одной прописной (a-z) и одной заглавной буквой (A-Z),"
            " минимум с одной цифрой (0-9) и одним специальным символом (!@#$%^&*)."
        )
