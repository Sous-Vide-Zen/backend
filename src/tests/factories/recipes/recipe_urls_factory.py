from collections import OrderedDict


def get_retrieve_url_data() -> dict:
    """Factory for test retrieving url."""
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
        "reactions_count": 0,
        "views_count": 0,
    }
    return recipe_data
