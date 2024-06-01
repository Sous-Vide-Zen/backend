from collections import OrderedDict


def get_create_comment_view_data():
    response_example_data = {
        "id": 1,
        "author": OrderedDict(
            [
                ("id", 1),
                ("username", "user1"),
                ("display_name", None),
                ("avatar", None),
            ]
        ),
        "text": "Test_comment",
    }
    return response_example_data
