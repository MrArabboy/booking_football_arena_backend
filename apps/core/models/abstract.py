from django.db import models


class CreatedAtAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class UpdatedAtAbstract(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedUpdatedAbstract(CreatedAtAbstract, UpdatedAtAbstract):
    class Meta:
        abstract = True
        ordering = ("-created_at",)


class IsActiveAbstract(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class OrderAbstract(models.Model):
    order = models.DecimalField(default=1, max_digits=10, decimal_places=2)

    class Meta:
        ordering = ("order",)
        abstract = True


class LocationAbstract(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    class Meta:
        abstract = True
