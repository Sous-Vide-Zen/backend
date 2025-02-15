from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

from src.base.code_text import (
    PASSWORD_MUST_CONTAIN_SPECIAL_CHARACTER,
    HELP_TEXT_FOR_PASSWORD,
    PASSWORD_MUST_CONTAIN_ONE_LOWERCASE,
    PASSWORD_MUST_CONTAIN_ONE_UPPERCASE_LETTER,
    PASSWORD_MUST_CONTAIN_ONE_NUMBER,
    SPECIAL_SYMBOLS,
)


class CustomPasswordValidator:
    def validate(self, password, user=None):
        pattern = f"[{re.escape(SPECIAL_SYMBOLS)}]"
        if not re.findall(pattern, password):
            raise ValidationError(
                _(PASSWORD_MUST_CONTAIN_SPECIAL_CHARACTER),
                code="password_no_special",
            )

    def get_help_text(self):
        return _(HELP_TEXT_FOR_PASSWORD)


class NoLowerCaseValidator:
    def validate(self, password, user=None):
        if not re.findall("[a-z, а-я]", password):
            raise ValidationError(
                _(PASSWORD_MUST_CONTAIN_ONE_LOWERCASE),
                code="password_no_lower",
            )

    def get_help_text(self):
        return _(PASSWORD_MUST_CONTAIN_ONE_LOWERCASE)


class NoUpperCaseValidator:
    def validate(self, password, user=None):
        if not re.findall("[A-Z, А-Я]", password):
            raise ValidationError(
                _(PASSWORD_MUST_CONTAIN_ONE_UPPERCASE_LETTER),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _(PASSWORD_MUST_CONTAIN_ONE_UPPERCASE_LETTER)


class NoNumbersValidator:
    def validate(self, password, user=None):
        if not re.findall("[0-9]", password):
            raise ValidationError(
                _(PASSWORD_MUST_CONTAIN_ONE_NUMBER),
                code="password_no_number",
            )

    def get_help_text(self):
        return _(PASSWORD_MUST_CONTAIN_ONE_NUMBER)
