from django.db import transaction
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.arena.api.v1.filters import FootballArenaFilter
from apps.arena.api.v1.permissions import IsAdminOrArenaManager
from apps.arena.api.v1.serializers import (
    FootballArenaCreateByAdminSerializer,
    FootballArenaCreateByArenaManagerSerializer,
    FootballArenaDetailSerializer,
    FootballArenaListSerializer,
)
from apps.arena.models import FootballArena
from apps.core.choices import UserRoleChoice


class FootballArenaViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = FootballArenaListSerializer
    queryset = FootballArena.objects.none()
    filterset_class = FootballArenaFilter
    search_fields = ("name", "address", "phone_number", "telegram_username", "description")

    def get_queryset(self):
        query_by_role = {
            UserRoleChoice.ADMIN: FootballArena.objects.all(),
            UserRoleChoice.ARENA_MANAGER: FootballArena.objects.filter(
                owner=self.request.user
            ),
            UserRoleChoice.USER: FootballArena.objects.filter(is_active=True),
        }
        return query_by_role[self.request.user.role]

    def get_permissions(self):
        if self.action in {"create", "partial_update", "destroy"}:
            self.permission_classes = [IsAuthenticated, IsAdminOrArenaManager]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in {"create", "partial_update"}:
            match self.request.user.role:
                case UserRoleChoice.ADMIN:
                    self.serializer_class = FootballArenaCreateByAdminSerializer
                case UserRoleChoice.ARENA_MANAGER:
                    self.serializer_class = FootballArenaCreateByArenaManagerSerializer
        elif self.action == "retrieve":
            self.serializer_class = FootballArenaDetailSerializer
        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
