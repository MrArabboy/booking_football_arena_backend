from django.contrib import admin

from apps.booking.models import FootballArenaBooking


@admin.register(FootballArenaBooking)
class FootballArenaBookingAdmin(admin.ModelAdmin):
    list_display = ("user", "arena", "start_date", "end_date", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "arena__name")
    raw_id_fields = ("user", "arena")
