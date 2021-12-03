from rest_framework import permissions

from users.models import CHOICES


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return(
            user.is_authenticated
            and (user.role == 'admin' or user.is_superuser)
        )


class ModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return(
            user.is_authenticated
            and (
                user.role == 'admin'
                or user.role == 'moderator'
                or user.is_superuser
            )
        )
