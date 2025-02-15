import pytest
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from src.base.code_text import (
    HELP_TEXT_FOR_PASSWORD,
    PASSWORD_MUST_CONTAIN_ONE_LOWERCASE,
    PASSWORD_MUST_CONTAIN_ONE_UPPERCASE_LETTER,
    PASSWORD_MUST_CONTAIN_ONE_NUMBER,
)
from src.base.validators import (
    CustomPasswordValidator,
    NoLowerCaseValidator,
    NoUpperCaseValidator,
    NoNumbersValidator,
)


@pytest.mark.parametrize(
    "password",
    [
        "short",
        "NOLOWERCASE123!",
        "nouppercase123!",
        "NoSpecial123",
        "NoNumbers!!",
        "ValidPassword123!",
    ],
)
def test_password_validators(password):
    """
    Test all configured password validators
    """
    # Если пароль "ValidPassword123!", то он должен быть действительным
    if password == "ValidPassword123!":
        # Пароль должен быть принят всеми валидаторами без ошибок
        try:
            validate_password(password)
        except ValidationError as e:
            pytest.fail(
                f"ValidPassword123! should be a valid password, but failed with {e}"
            )
    else:
        # Для всех остальных паролей ожидаем ValidationError
        with pytest.raises(ValidationError):
            validate_password(password)


@pytest.mark.parametrize(
    "validator_class, expected_help_text",
    [
        (CustomPasswordValidator, HELP_TEXT_FOR_PASSWORD),
        (
            NoLowerCaseValidator,
            PASSWORD_MUST_CONTAIN_ONE_LOWERCASE,
        ),
        (
            NoUpperCaseValidator,
            PASSWORD_MUST_CONTAIN_ONE_UPPERCASE_LETTER,
        ),
        (NoNumbersValidator, PASSWORD_MUST_CONTAIN_ONE_NUMBER),
    ],
)
def test_validator_help_texts(validator_class, expected_help_text):
    validator = validator_class()
    help_text = validator.get_help_text()
    assert (
        help_text == expected_help_text
    ), f"{validator_class.__name__} help text did not match expected"
