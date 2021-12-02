from rest_framework import permissions

from users.models import CHOICES


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and (
                        request.user.is_staff or request.user.role
                        == 'ADMIN')
                    )
