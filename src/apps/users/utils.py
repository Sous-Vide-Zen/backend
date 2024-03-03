import random
from typing import Type
from django.db import models


def generate_username(user_id: int, user_model: Type[models.Model]) -> str:
    """
    Генерирует уникальное имя пользователя.

    Args:
        user_id: Идентификатор пользователя.
        user_model: Класс модели пользователя для проверки уникальности имени пользователя.

    Returns:
        Строка с уникальным именем пользователя.
    """
    base_username = f"user{user_id}"
    if not user_model.objects.filter(username=base_username).exists():
        return base_username
    else:
        while True:
            random_number = random.randint(100000, 999999)
            new_username = f"user{random_number}"
            if not user_model.objects.filter(username=new_username).exists():
                return new_username
