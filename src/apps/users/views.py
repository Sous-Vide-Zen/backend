from rest_framework.exceptions import NotFound
from src.base.permissions import IsOwnerOrAdminOrReadOnly
from rest_framework import viewsets, status
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import CustomUserSerializer
from drf_yasg.utils import swagger_auto_schema


from djoser.views import UserViewSet


class CustomUserMeViewSet(UserViewSet):
    @swagger_auto_schema(exclude=["update", "partial_update", "destroy"])
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        raise NotFound("Endpoint is disabled.")

    def update(self, request, *args, **kwargs):
        raise NotFound("Endpoint is disabled.")

    def partial_update(self, request, *args, **kwargs):
        raise NotFound("Endpoint is disabled.")

    def destroy(self, request, *args, **kwargs):
        raise NotFound("Endpoint is disabled.")


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    lookup_field = "username"
