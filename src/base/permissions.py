from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import exception_handler

from src.base.code_text import CREDENTIALS_WERE_NOT_PROVIDED, DONT_HAVE_PERMISSIONS


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Permission to allow only the object owner or administrator access to modify. .
    Read access can be unauthorized
    """

    def has_object_permission(self, request, view, obj):
        """
        Permission to allow only the object owner or administrator access to modify. .
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return obj == request.user or getattr(request.user, "is_admin", False)

        return False


class IsObjectOwnerOrAdminOrReadOnly(BasePermission):
    """
    Permission to allow only the object author or administrator access to modify. .
    Read access can be unauthorized
    """

    def has_object_permission(self, request, view, obj):
        """
        Permission to allow only the object author or administrator access to modify. .
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return obj.author == request.user or getattr(
                request.user, "is_admin", False
            )

        return False


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    Permission to allow only the object owner or staff access to modify. .
    Read access can be unauthorized
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_staff


def custom_exception_handler(exc, context):
    """
    User handler for answers of the exceptions of the API.
    """

    response = exception_handler(exc, context)

    if (
        response.status_code == 401
        and response.data.get("detail")
        == "Authentication credentials were not provided."
    ):
        response.data = CREDENTIALS_WERE_NOT_PROVIDED
    if (
        response.status_code == 403
        and response.data.get("detail")
        == "You do not have permission to perform this action."
    ):
        response.data = DONT_HAVE_PERMISSIONS
    return response
