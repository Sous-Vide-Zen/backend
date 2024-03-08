import pytest
from django.core.exceptions import ValidationError

from src.apps.users.validators import CustomPasswordValidator


@pytest.mark.parametrize(
    "password",
    [
        "short",
        "NOLOWERCASE123!a",
        "nouppercase123!",
        "NoSpecial123",
        "NoNumbers!!",
        "ValidPassword123!",
    ],
)
def test_password_validator(password):
    validator = CustomPasswordValidator()

    if password == "ValidPassword123!":
        # Данный пароль должен быть корректным, ожидаем, что ошибок не будет
        assert validator.validate(password) is None
    else:
        # Для всех остальных паролей ожидаем ValidationError
        with pytest.raises(ValidationError):
            validator.validate(password)
