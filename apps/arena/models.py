from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_minio_backend import MinioBackend

from apps.core.models.abstract import (
    CreatedUpdatedAbstract,
    IsActiveAbstract,
    LocationAbstract,
    OrderAbstract,
)


class FootballArena(
    IsActiveAbstract, LocationAbstract, OrderAbstract, CreatedUpdatedAbstract
):
    owner = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="football_areas"
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    telegram_username = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(
        storage=MinioBackend(
            bucket_name=settings.PUBLIC_BUCKET_NAME,
        ),
        upload_to=settings.FOOTBALL_AREA_FILE_UPLOAD_PATH,
    )
    cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ("order",)
        verbose_name = _("Football Arena")
        verbose_name_plural = _("Football Arenas")

    def __str__(self):
        return self.name


class FootballArenaImage(OrderAbstract, CreatedUpdatedAbstract):
    area = models.ForeignKey(
        "arena.FootballArena", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        storage=MinioBackend(
            bucket_name=settings.PUBLIC_BUCKET_NAME,
        ),
        upload_to=settings.FOOTBALL_AREA_FILE_UPLOAD_PATH,
    )

    class Meta:
        ordering = (
            "area",
            "order",
        )
        verbose_name = _("Football Arena Image")
        verbose_name_plural = _("Football Arena Images")

    def __str__(self):
        return self.image.name
