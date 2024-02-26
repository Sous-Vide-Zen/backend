from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Permission to allow only the object owner or administrator access to modify. .
    Read access can be unauthorized
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.admin


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    Permission to allow only the object owner or staff access to modify. .
    Read access can be unauthorized
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_staff
