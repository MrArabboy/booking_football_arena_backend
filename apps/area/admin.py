from django.contrib import admin

from .models import FootballArea, FootballAreaImage


@admin.register(FootballArea)
class FootballAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)
    raw_id_fields = ("owner",)


@admin.register(FootballAreaImage)
class FootballAreaImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "area", "order", "created_at", "updated_at")
    search_fields = ("area__name", "image__name")
    raw_id_fields = ("area",)
