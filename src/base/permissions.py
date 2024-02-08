from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Пермишн, позволяющий доступ на изменение только владельцу объекта или администратору. .
    На чтение можно быть неавторизованным
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить доступ на чтение всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить доступ на изменение только владельцам объектов или администраторам
        return obj == request.user or request.user.is_staff
