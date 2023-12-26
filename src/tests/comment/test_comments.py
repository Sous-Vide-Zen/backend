import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from src.apps.comments.models import Comment
import datetime


@pytest.mark.django_db
class TestCommentModel:
    def test_comment_creation(self, new_user, new_recipe):
        # Проверяет, что комментарий успешно создается
        # с заданными автором, рецептом и текстом
        comment = Comment.objects.create(
            author=new_user, recipe=new_recipe, text="Test Comment"
        )
        assert comment.author == new_user
        assert comment.recipe == new_recipe
        assert comment.text == "Test Comment"

    def test_comment_validation(self, new_user, new_recipe):

        long_text = "x" * 1001
        comment = Comment(author=new_user, recipe=new_recipe, text=long_text)

        with pytest.raises(ValidationError):
            comment.full_clean()

    def test_comment_hierarchy(self, new_user, new_recipe):
        # Создает родительский и дочерний комментарии, проверяя,
        # что дочерний комментарий правильно ссылается на свой родительский комментарий.
        parent_comment = Comment.objects.create(
            author=new_user, recipe=new_recipe, text="Parent Comment"
        )
        child_comment = Comment.objects.create(
            author=new_user,
            recipe=new_recipe,
            text="Child Comment",
            parent=parent_comment,
        )
        assert child_comment.parent == parent_comment

    def test_comment_relationships(self, new_user, new_recipe):
        # Проверяет, что связи комментария с автором и рецептом
        # работают корректно. Утверждает, что созданный комментарий имеет правильные ссылки на автора и рецепт.
        comment = Comment.objects.create(
            author=new_user, recipe=new_recipe, text="Test Comment"
        )
        assert comment.author == new_user
        assert comment.recipe == new_recipe

    def test_comment_publication_date(self, new_user, new_recipe):
        comment = Comment.objects.create(
            author=new_user, recipe=new_recipe, text="Test Comment"
        )
        assert comment.pub_date <= timezone.now()
        assert isinstance(comment.pub_date, datetime.datetime)

    def test_set_null_on_delete_recipe(self, new_user, new_recipe):
        # Проверяет, что при удалении рецепта связанный с ним комментарий
        # не удаляется, а его поле recipe устанавливается в null
        comment = Comment.objects.create(
            author=new_user, recipe=new_recipe, text="Test Comment"
        )
        new_recipe.delete()
        comment.refresh_from_db()
        assert comment.recipe is None

    def test_set_null_on_delete_author(self, new_user, new_recipe):
        # проверяет поведение при удалении автора комментария.
        # Убеждается, что поле author устанавливается в null, когда связанный пользователь удаляется.
        comment = Comment.objects.create(
            author=new_user, recipe=new_recipe, text="Test Comment"
        )
        new_user.delete()
        comment.refresh_from_db()
        assert comment.author is None