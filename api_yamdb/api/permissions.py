from rest_framework import permissions
from users.models import UserRoles


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return(
            user.is_authenticated
            and (user.role == UserRoles.ADMIN or user.is_superuser)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if not user.is_anonymous:
            return (
                user.role == UserRoles.ADMIN or user.is_superuser
            )
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if not user.is_anonymous:
            return (
                user.role == UserRoles.ADMIN or user.is_superuser
            )
        return False


class AuthorOrAdminOrModeratorReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or user.role == UserRoles.ADMIN
                or user.is_superuser
                or user.role == UserRoles.MODERATOR)
