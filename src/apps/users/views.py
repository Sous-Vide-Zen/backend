from rest_framework.response import Response
from src.base.permissions import IsOwnerOrAdminOrReadOnly
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserMeSerializer
from drf_yasg.utils import swagger_auto_schema

from djoser.views import UserViewSet


class CustomUserMeViewSet(UserViewSet):
    """
    Переопределение стандартного ViewSet из библиотеки Djoser для кастомизации поведения и ответов API,
    связанных с текущим пользователем.
    Особенности:
    - Переопределяет кастомное действие `me` для получения данных текущего пользователя.
    - Отключает стандартные действия обновления и удаления, делая их недоступными через API.
    """

    @swagger_auto_schema(methods=["get"], responses={200: CustomUserMeSerializer})
    @action(methods=["get"], detail=False)
    def me(self, request: Request, *args, **kwargs):
        #     """
        # Декоратор @action используется для определения кастомного действия в ViewSet
        #
        # В данном контексте, @action настраивает действие 'me', которое:
        # - Обрабатывает только GET-запросы (указано в параметре methods).
        # """
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        """Переопределение встроенного сериализатора для возвращения касмтоного"""
        if self.action == "me":
            return CustomUserMeSerializer
        return super().get_serializer_class()

    def get_object(self):
        """
        Переопределяет метод получения объекта для текущего действия.

        Для действия 'me', возвращает текущего аутентифицированного пользователя без необходимости
        указывать его идентификатор в URL, обходя стандартное ожидание DRF о наличии идентификатора объекта.
        Это позволяет обрабатывать запросы к действию 'me', предназначенному для получения данных профиля
        текущего пользователя, без ошибок связанных с отсутствием 'id' в URL запроса.
        """
        if self.action == "me":
            return self.request.user
        return super().get_object()

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """Override the retrieve method to disable it for non-me actions."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request: Request, *args, **kwargs) -> Response:
        """Disable update action."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """Disable partial update action."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Disable destroy action."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing users.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    lookup_field = "username"
    http_method_names = ["get", "patch", "delete"]
