from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Пермишн, позволяющий доступ только владельцу объекта или администратору.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение только владельцу объекта или администратору
        return obj == request.user or request.user.is_staff
