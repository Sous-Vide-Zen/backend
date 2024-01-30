from src.apps.users.permissions import IsOwnerOrAdmin
from rest_framework import viewsets, status
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import CustomUserSerializer
from djoser.views import UserViewSet


class CustomUserMeViewSet(UserViewSet):
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        # Переопределение метода retrieve для получения данных текущего пользователя
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = "username"
