from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.booking.api.v1.filters import BookingFilter
from apps.booking.api.v1.permissions import (
    BookingCancelPermission,
    BookingConfirmPermission,
)
from apps.booking.api.v1.serializers import BookingCreateSerializer, BookingListSerializer
from apps.booking.api.v1.services import calculate_booking_price, check_arena_availability
from apps.booking.models import BookingStatusChoice, FootballArenaBooking
from apps.core.choices import UserRoleChoice
from apps.core.exceptions import BaseAPIException


class BookingViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = FootballArenaBooking.objects.none()
    serializer_class = BookingListSerializer
    filterset_class = BookingFilter

    def get_queryset(self):
        queryset_by_role = {
            UserRoleChoice.ADMIN: FootballArenaBooking.objects.all(),
            UserRoleChoice.ARENA_MANAGER: FootballArenaBooking.objects.filter(
                arena__owner=self.request.user
            ),
            UserRoleChoice.USER: FootballArenaBooking.objects.filter(
                user=self.request.user
            ),
        }
        return queryset_by_role[self.request.user.role]

    def get_permissions(self):
        if self.action == "cancel":
            self.permission_classes = [IsAuthenticated, BookingCancelPermission]
        elif self.action == "confirm":
            self.permission_classes = [IsAuthenticated, BookingConfirmPermission]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = BookingCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if not check_arena_availability(
            validated_data["arena"],
            validated_data["start_date"],
            validated_data["end_date"],
        ):
            raise BaseAPIException(
                message=_("Arena was already booked for this time"),
            )
        serializer.save(
            total_price=calculate_booking_price(
                validated_data["arena"],
                validated_data["start_date"],
                validated_data["end_date"],
            ),
        )
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def cancel(self, *args, **kwargs):
        booking = self.get_object()
        booking.status = BookingStatusChoice.CANCELLED
        booking.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def confirm(self, *args, **kwargs):
        booking = self.get_object()
        booking.status = BookingStatusChoice.CONFIRMED
        booking.save()
        return Response(status=status.HTTP_200_OK)
