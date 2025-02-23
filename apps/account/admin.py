from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "role", "created_at"]
    list_filter = ["is_active", "is_superuser", "role"]
    search_fields = [
        "username",
        "full_name",
    ]
    readonly_fields = ["created_at"]
    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "created_at")}),
    )
    add_fieldsets = (
        (
            "Registration",
            {
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
