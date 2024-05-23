import datetime
import pytest
from django.utils import dateparse
from collections import OrderedDict

from src.base.code_text import (
    PAGE_NOT_FOUND,
    CREDENTIALS_WERE_NOT_PROVIDED,
    COMMENT_NOT_FOUND,
    INVALID_ID_FORMAT,
    DONT_HAVE_PERMISSIONS,
    CANT_EDIT_COMMENT,
    COMMENT_SUCCESSFULLY_DELETE,
)
from src.apps.comments.models import Comment
from unittest import mock


@pytest.mark.django_db
@pytest.mark.api
class TestCommentUrls:
    """
    Test comment urls
    """

    def test_list_comments(self, client, new_comment, new_recipe):
        """
        Test for list of comments page
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """

        example_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                OrderedDict(
                    [
                        ("id", new_comment.id),
                        (
                            "author",
                            OrderedDict(
                                [
                                    ("id", new_comment.author.id),
                                    ("username", new_comment.author.username),
                                    ("display_name", None),
                                    ("avatar", None),
                                ]
                            ),
                        ),
                        ("text", new_comment.text),
                    ]
                )
            ],
        }
        slug = new_recipe.slug
        response = client.get(f"/api/v1/recipe/{slug}/comments/")

        assert response.status_code == 200

        response_data = response.data.copy()
        results = response_data.get("results")
        results[0].pop("updated_date")
        results[0].pop("pub_date")

        assert response_data == example_data

    def test_list_comments_not_found(self, client):
        """
        Test of not found list of comments for non-existing recipe
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """
        response = client.get("/api/v1/recipe/not-found/")

        assert response.status_code == 404
        assert response.data == PAGE_NOT_FOUND

    def test_create_comment_to_recipe(self, api_client, new_author, new_recipe):
        """
        Test for creation of a comment to recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """

        comment_data = {"text": "Test_comment"}
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/"
        api_client.force_authenticate(user=new_author)
        response = api_client.post(url, data=comment_data, format="json")

        assert Comment.objects.filter(
            text=comment_data.get("text"), author=new_author, recipe=new_recipe
        ).exists()
        assert response.status_code == 201

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
        response_data = response.data.copy()
        response_data.pop("pub_date", None)
        response_data.pop("updated_date", None)

        assert response_data == response_example_data

    def test_create_comment_to_non_existing_recipe(self, api_client, new_author):
        """
        Test for creation of a comment to non-existing recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """
        comment_data = {"text": "Test_comment"}
        url = f"/api/v1/recipe/non-existing-recipe/comments/"
        api_client.force_authenticate(user=new_author)
        response = api_client.post(url, data=comment_data, format="json")

        assert response.status_code == 404
        assert response.data == PAGE_NOT_FOUND

    def test_create_comment_to_recipe_unauthorized(self, api_client, new_recipe):
        """
        Test for creation of a comment by unauthorized user
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """
        comment_data = {"text": "Test_comment"}
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/"
        response = api_client.post(url, data=comment_data, format="json")

        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED

    def test_create_comment_to_recipe_no_text(self, api_client, new_author, new_recipe):
        """
        Test for creation of a comment with no text indicated
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """
        comment_data = {"text": ""}
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/"
        api_client.force_authenticate(user=new_author)
        response = api_client.post(url, data=comment_data, format="json")

        assert response.status_code == 400

    def test_create_comment_to_recipe_too_long_text(
        self, api_client, new_author, new_recipe
    ):
        """
        Test for creation of a comment with too long text
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """
        comment_text = "s" * 1001
        comment_data = {"text": comment_text}
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/"
        api_client.force_authenticate(user=new_author)
        response = api_client.post(url, data=comment_data, format="json")

        assert len(comment_text) > 1000
        assert response.status_code == 400

    def test_create_comment_to_comment_wrong_parent_format(
        self, api_client, new_author, new_recipe, new_comment
    ):
        """
        Test for creation of a comment to comment indicating parent field.
        Response 404 if wrong format of parent field and 201 if right format.

        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/
        """
        comment_data = {"text": "Test_comment", "parent": "str"}
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/"
        api_client.force_authenticate(user=new_author)
        response = api_client.post(url, data=comment_data, format="json")

        assert response.status_code == 400

        comment_data = {"text": "Test_comment_to_comment", "parent": new_comment.id}
        response = api_client.post(url, data=comment_data, format="json")

        assert response.status_code == 201
        assert len(new_recipe.comments.all()) == 2
        assert new_recipe.comments.filter(text="Test_comment_to_comment").exists()

    def test_update_comment_to_recipe(
        self, api_client, new_user, new_recipe, new_comment
    ):
        """
        Test for update of a comment to recipe
        [PUT] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        comment_data = {"text": "Test_comment_updated"}
        slug = new_recipe.slug
        new_comment_id = new_comment.id
        url = f"/api/v1/recipe/{slug}/comments/{new_comment_id}/"
        api_client.force_authenticate(user=new_user)
        response = api_client.put(url, data=comment_data, format="json")
        new_comment.refresh_from_db()

        assert new_comment.text == "Test_comment_updated"
        assert Comment.objects.filter(
            text=comment_data.get("text"), author=new_user, recipe=new_recipe
        ).exists()
        assert response.status_code == 200

        updated_comment_example_data = {
            "id": new_comment.id,
            "author": OrderedDict(
                [
                    ("id", new_comment.author.id),
                    ("username", new_comment.author.username),
                    ("display_name", None),
                    ("avatar", None),
                ]
            ),
            "text": new_comment.text,
        }
        response_data = response.data.copy()
        response_data.pop("updated_date", None)
        response_data.pop("pub_date", None)

        assert response_data == updated_comment_example_data

    def test_update_comment_recipe_not_found(self, api_client, new_user, new_comment):
        """
        Test for updating of a comment to non-existing recipe
        [PUT] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        comment_data = {"text": "Test_comment"}
        url = f"/api/v1/recipe/non-existing-recipe/comments/{new_comment.id}/"
        api_client.force_authenticate(user=new_user)
        response = api_client.put(url, data=comment_data, format="json")

        assert response.status_code == 404
        assert response.data == PAGE_NOT_FOUND

    def test_update_comment_id_not_found(
        self, api_client, new_user, new_recipe, new_comment
    ):
        """
        Test for updating of a comment to non-existing comment
        [PUT] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        comment_data = {"text": "Test_comment"}
        url = f"/api/v1/recipe/{new_recipe.slug}/comments/100/"
        api_client.force_authenticate(user=new_user)
        response = api_client.put(url, data=comment_data, format="json")

        assert response.status_code == 404
        assert response.data == COMMENT_NOT_FOUND

    def test_update_comment_wrong_id_format(
        self, api_client, new_user, new_recipe, new_comment
    ):
        """
        Test for updating of a comment with wrong id format
        [PUT] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        comment_data = {"text": "Test_comment"}
        url = f"/api/v1/recipe/{new_recipe.slug}/comments/some_str/"
        api_client.force_authenticate(user=new_user)
        response = api_client.put(url, data=comment_data, format="json")

        assert response.status_code == 400
        assert response.data == INVALID_ID_FORMAT

    def test_update_comment_to_recipe_unauthorized(
        self, api_client, new_recipe, new_comment
    ):
        """
        Test for update of a comment to recipe by aunauthorized user
        [PUT] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        comment_data = {"text": "Test_comment_updated"}
        slug = new_recipe.slug
        new_comment_id = new_comment.id
        url = f"/api/v1/recipe/{slug}/comments/{new_comment_id}/"
        response = api_client.put(url, data=comment_data, format="json")
        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED

    def test_update_other_user_comment_to_recipe(
        self, api_client, new_author, new_recipe, new_comment
    ):
        """
        Test for update of a comment not by its author
        [PUT] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        comment_data = {"text": "Test_comment"}
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/{new_comment.id}/"
        api_client.force_authenticate(user=new_author)
        response = api_client.put(url, data=comment_data, format="json")

        assert response.status_code == 403
        assert response.data == DONT_HAVE_PERMISSIONS

    def test_update_comment_created_more_than_1_day_before(
        self, api_client, new_user, new_recipe
    ):
        """
        Test for update a comment which created >= 1 day before
        [PUT] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        with mock.patch("django.utils.timezone.now") as mock_now:
            test_pub_date = datetime.datetime.now() - datetime.timedelta(hours=25)
            mock_now.return_value = dateparse.parse_datetime(str(test_pub_date))
            new_comment = Comment.objects.create(
                recipe=new_recipe, text="Test_comment_on_recipe", author=new_user
            )
        comment_data = {"text": "Test_comment_on_recipe_update"}
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/{new_comment.id}/"
        api_client.force_authenticate(user=new_user)
        response = api_client.put(url, data=comment_data, format="json")

        assert response.status_code == 403
        assert response.data == CANT_EDIT_COMMENT

    def test_comment_delete(self, api_client, new_user, new_recipe, new_comment):
        """
        Test for deleting a comment
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/{new_comment.id}/"
        api_client.force_authenticate(user=new_user)
        response = api_client.delete(url)

        assert response.status_code == 204
        assert response.data == COMMENT_SUCCESSFULLY_DELETE
        assert not Comment.objects.filter(id=new_comment.id).exists()

    def test_comment_delete_by_not_author(
        self, api_client, new_author, new_recipe, new_comment
    ):
        """
        Test for deleting a comment by user that is not its author
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/comments/{id}/
        """
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/comments/{new_comment.id}/"
        api_client.force_authenticate(user=new_author)
        response = api_client.delete(url)

        assert response.status_code == 403
        assert response.data == DONT_HAVE_PERMISSIONS
