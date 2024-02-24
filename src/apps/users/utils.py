import random


def generate_username(user_id):
    from .models import (
        CustomUser,
    )  # Отложенный импорт для избежания циклического импорта

    base_username = f"user{user_id}"
    if not CustomUser.objects.filter(username=base_username).exists():
        return base_username
    else:
        random_number = random.randint(100000, 999999)
        new_username = f"user{random_number}"
        while CustomUser.objects.filter(username=new_username).exists():
            random_number = random.randint(100000, 999999)
            new_username = f"user{random_number}"
        return new_username
