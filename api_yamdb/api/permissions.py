from rest_framework import permissions
from users.models import UserRoles


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return(
            user.is_authenticated
            and (user.role == UserRoles.ADMIN or user.is_superuser)
        )


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
