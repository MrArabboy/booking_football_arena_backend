from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from apps.account.managers import UserManager
from apps.core.choices import UserRoleChoice
from apps.core.models.abstract import CreatedUpdatedAbstract
from apps.core.models.fields import ConcatenateFields


class User(AbstractBaseUser, PermissionsMixin, CreatedUpdatedAbstract):
    username = models.CharField(
        max_length=150, unique=True, validators=[UnicodeUsernameValidator()]
    )
    role = models.CharField(
        max_length=20, choices=UserRoleChoice.choices, default=UserRoleChoice.USER
    )
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.GeneratedField(
        expression=ConcatenateFields(
            models.F("last_name"),
            models.Value(" "),
            models.F("first_name"),
            models.Value(" "),
            models.F("middle_name"),
        ),
        output_field=models.CharField(max_length=150),
        db_persist=True,
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username
