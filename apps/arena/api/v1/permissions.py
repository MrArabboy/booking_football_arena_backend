from rest_framework.permissions import BasePermission

from apps.account.models import UserRoleChoice


class IsAdminOrArenaManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [UserRoleChoice.ADMIN, UserRoleChoice.ARENA_MANAGER]

    def has_object_permission(self, request, view, obj):
        return request.user.role == UserRoleChoice.ADMIN or obj.owner == request.user
