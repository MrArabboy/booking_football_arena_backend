from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.arena.models import FootballArena
from apps.booking.models import FootballArenaBooking
from apps.core.exceptions import BaseAPIException


class BookingListSerializer(serializers.ModelSerializer):
    arena = serializers.StringRelatedField()

    class Meta:
        model = FootballArenaBooking
        fields = (
            "id",
            "arena",
            "start_date",
            "end_date",
            "status",
            "total_price",
            "created_at",
        )


class BookingCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    arena = serializers.PrimaryKeyRelatedField(
        queryset=FootballArena.objects.filter(is_active=True)
    )
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def validate(self, attrs):
        if attrs["start_date"] >= attrs["end_date"]:
            raise BaseAPIException(
                message=_("Start date must be before end date"),
            )

        return attrs

    def create(self, validated_data):
        booking = FootballArenaBooking.objects.create(**validated_data)
        return booking
