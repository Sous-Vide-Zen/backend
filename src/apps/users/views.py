from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from src.base.permissions import IsOwnerOrAdminOrReadOnly
from rest_framework import viewsets, status
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserMeSerializer
from drf_yasg.utils import swagger_auto_schema


from djoser.views import UserViewSet


class CustomUserMeViewSet(UserViewSet):
    @swagger_auto_schema(methods=["get"], responses={200: CustomUserMeSerializer})
    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "me":
            return CustomUserMeSerializer
        return super().get_serializer_class()

    def get_object(self):
        # Возвращает объект текущего пользователя для действия 'me'
        if self.action == "me":
            return self.request.user
        return super().get_object()

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        if getattr(self, "current_action", None) == "me":
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    lookup_field = "username"
    http_method_names = ["get", "put", "patch", "delete", "head", "options", "trace"]
