from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserMeSerializer
from djoser.views import UserViewSet


class CustomUserMeViewSet(UserViewSet):

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_object(self):
        username = self.kwargs[self.lookup_field]
        return get_object_or_404(self.get_queryset(), **{self.lookup_field: username})

    def retrieve(self, request, *args, **kwargs):
        # Переопределение метода retrieve для просмотра данных пользователя
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Переопределение метода partial_update для частичного обновления данных пользователя
        instance = self.get_object()
        if not (request.user == instance or request.user.is_staff):
            return Response("You don't have permission to update this user's data.")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Переопределение метода destroy для удаления пользователя
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
