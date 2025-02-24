from django_filters import FilterSet, filters

from apps.arena.models import FootballArena
from apps.booking.models import BookingStatusChoice


class BookingFilter(FilterSet):
    arena = filters.ModelChoiceFilter(queryset=FootballArena.objects.all())
    status = filters.ChoiceFilter(choices=BookingStatusChoice.choices)
