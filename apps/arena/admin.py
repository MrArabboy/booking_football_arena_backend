from django.contrib import admin

from .models import FootballArena, FootballArenaImage


@admin.register(FootballArena)
class FootballArenaAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)
    raw_id_fields = ("owner",)


@admin.register(FootballArenaImage)
class FootballArenaImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "arena", "order", "created_at", "updated_at")
    search_fields = ("arena__name", "image__name")
    raw_id_fields = ("arena",)
