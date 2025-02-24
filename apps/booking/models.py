from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.choices import BookingStatusChoice
from apps.core.models.abstract import CreatedUpdatedAbstract


class FootballArenaBooking(CreatedUpdatedAbstract):
    arena = models.ForeignKey(
        "arena.FootballArena", on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="bookings"
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=255,
        choices=BookingStatusChoice.choices,
        default=BookingStatusChoice.PENDING,
    )

    def __str__(self):
        return f"{self.user.username} - {self.arena.name}"

    class Meta:
        verbose_name = _("Football Arena Booking")
        verbose_name_plural = _("Football Arena Bookings")
        ordering = ["-created_at"]
