from django.db import models
from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin
from django_filters import FilterSet, filters

from apps.core.choices import BookingStatusChoice


class FootballArenaFilter(FilterSet):
    lat_long = filters.CharFilter(method="filter_lat_long")
    time_range = filters.DateTimeFromToRangeFilter(method="filter_time_range")

    def filter_lat_long(self, queryset, _, value):
        try:
            lat, long = map(float, value.split(","))  # pylint: disable=bad-builtin

            # Convert latitude and longitude to radians
            lat_rad = Radians(lat)
            long_rad = Radians(long)
            lat_field_rad = Radians(F("latitude"))
            long_field_rad = Radians(F("longitude"))

            # Calculate distance using Haversine formula
            # R * arccos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(long2 - long1))
            # where R is Earth's radius in kilometers (≈ 6371)
            distance = 6371 * ACos(
                Sin(lat_rad) * Sin(lat_field_rad)
                + Cos(lat_rad) * Cos(lat_field_rad) * Cos(long_field_rad - long_rad),
                output_field=models.FloatField(),  # Specify output field type
            )

            # Annotate queryset with distance and order by nearest first
            return queryset.annotate(distance=distance).order_by("distance")
        except ValueError:
            return queryset.none()

    def filter_time_range(self, queryset, _, value):
        if not value.start or not value.stop:
            return queryset

        return queryset.exclude(
            bookings__start_time__lt=value.stop,
            bookings__end_time__gt=value.start,
            bookings__status=BookingStatusChoice.CANCELLED,
        )
