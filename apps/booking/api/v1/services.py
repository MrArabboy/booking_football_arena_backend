from datetime import datetime
from decimal import Decimal

from apps.arena.models import FootballArena
from apps.booking.models import BookingStatusChoice, FootballArenaBooking


def check_arena_availability(
    arena: FootballArena, start_date: datetime, end_date: datetime
) -> bool:
    return (
        not FootballArenaBooking.objects.filter(
            arena=arena,
            start_date__lte=end_date,
            end_date__gte=start_date,
        )
        .exclude(status=BookingStatusChoice.CANCELLED)
        .exists()
    )


def calculate_booking_price(
    arena: FootballArena, start_date: datetime, end_date: datetime
) -> float:
    return arena.cost_per_hour * Decimal((end_date - start_date).total_seconds() / 3600)
