from rest_framework.permissions import BasePermission

from apps.account.models import User
from apps.core.choices import BookingStatusChoice, UserRoleChoice


class BookingCancelPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user: User = request.user
        return (
            obj.user == user or obj.arena.owner == user or user.role == UserRoleChoice.ADMIN
        )


class BookingConfirmPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user: User = request.user
        return obj.status == BookingStatusChoice.PENDING and (
            user.role == UserRoleChoice.ADMIN or obj.arena.owner == user
        )
