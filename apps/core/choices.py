from django.db import models


class UserRoleChoice(models.TextChoices):
    ADMIN = "admin"
    USER = "user"
    ARENA_MANAGER = "arena_manager"
