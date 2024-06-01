from collections import OrderedDict
from typing import Tuple, Dict, List


def get_recipe_data() -> dict:
    """Factory for test retrieving recipe serializer."""
    recipe_data = {
        "id": 1,
        "title": "Test Recipe",
        "slug": "test-recipe",
        "author": OrderedDict(
            [
                ("id", 1),
                ("username", "user1"),
                ("display_name", None),
                ("avatar", None),
            ]
        ),
        "preview_image": None,
        "ingredients": [],
        "full_text": "This is a test recipe full text.",
        "tag": [],
        "category": [],
        "cooking_time": 30,
    }
    return recipe_data


def get_create_data() -> tuple[
    dict[
        str,
        None
        | str
        | list[dict[str, str | int] | dict[str, str | int]]
        | int
        | list[str]
        | list[int],
    ],
    dict[
        str,
        None
        | str
        | list[dict[str, str | int] | dict[str, str | int]]
        | int
        | list[dict[str, str] | dict[str, str] | dict[str, str]]
        | list[int],
    ],
]:
    """Factory for test creating recipe serializer."""
    example_data = {
        "title": "Delicious Recipe",
        "slug": "delicious-recipe",
        "preview_image": None,
        "ingredients": [
            {"name": "Water", "unit": "литр", "amount": 1},
            {"name": "Сахар", "unit": "грамм", "amount": 500},
        ],
        "full_text": "Heat the oven to 180°C fan/gas 6. Separate the "
        "leaves from the cauliflower and cut the florets "
        "into 3-4cm chunks, spreading them out on a baking "
        "tray as you work. Chop the central stalk into "
        "similar sized chunks and add to the tray too. Strip "
        "the leaves from their stems (reserving the leaves), "
        "halve the stems and add them to the tray. Season, "
        "drizzle with half the oil, then roast for 25 "
        "minutes.",
        "tag": ["Горячий", "вода", "сахар"],
        "cooking_time": 30,
        "category": [2],
    }

    example_response = {
        "id": 1,
        "title": "Delicious Recipe",
        "slug": "delicious-recipe",
        "preview_image": None,
        "ingredients": [
            {"name": "Water", "unit": "литр", "amount": 1},
            {"name": "Сахар", "unit": "грамм", "amount": 500},
        ],
        "full_text": "Heat the oven to 180°C fan/gas 6. Separate the "
        "leaves from the cauliflower and cut the florets "
        "into 3-4cm chunks, spreading them out on a baking "
        "tray as you work. Chop the central stalk into "
        "similar sized chunks and add to the tray too. Strip "
        "the leaves from their stems (reserving the leaves), "
        "halve the stems and add them to the tray. Season, "
        "drizzle with half the oil, then roast for 25 "
        "minutes.",
        "tag": [
            {"name": "Горячий", "slug": "goriachii"},
            {"name": "вода", "slug": "voda"},
            {"name": "сахар", "slug": "sakhar"},
        ],
        "category": [2],
        "cooking_time": 30,
    }
    return example_data, example_response


def get_update_data() -> dict:
    """Factory for test updating recipe serializers."""
    example_data = {
        "title": "Updated Recipe",
        "slug": "updated-recipe",
        "preview_image": None,
        "ingredients": [
            {"name": "Water", "unit": "литр", "amount": 1},
            {"name": "Сахар", "unit": "грамм", "amount": 500},
        ],
        "full_text": "This is an updated recipe full text.",
        "tag": ["Горячий", "вода", "сахар"],
        "category": [2],
        "cooking_time": 20,
    }
    return example_data
