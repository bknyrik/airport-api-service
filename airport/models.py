from __future__ import annotations
import os
import uuid
from typing import Iterable

from django.db import models
from django.db.models import constraints
from django.db.models import Q, F
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def create_custom_image_path(
    instance: Airport | Airplane,
    file_name: str
) -> str:
    _, ext = os.path.splitext(file_name)
    return os.path.join(
        "upload/images/",
        f"{slugify(instance.name)}-{uuid.uuid4()}{ext}"
    )


class Facility(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=False, default="", max_length=64)

    class Meta:
        verbose_name_plural = "facilities"
        ordering = ("name",)

    def save(
        self,
        *,
        force_insert: bool | tuple[models.base.ModelBase, ...] = False,
        force_update: bool = False,
        using: str = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.slug = slugify(self.name)

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self) -> str:
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(null=False, default="", max_length=64)

    class Meta:
        db_table = "airport_airplane_type"
        ordering = ("name",)

    def save(
        self,
        *,
        force_insert: bool | tuple[models.base.ModelBase, ...] = False,
        force_update: bool = False,
        using: str = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.slug = slugify(self.name)

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=64, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )
    facilities = models.ManyToManyField(
        Facility,
        related_name="airplanes"
    )
    image = models.ImageField(null=True, upload_to=create_custom_image_path)
    slug = models.SlugField(null=False, default="", max_length=64)

    class Meta:
        ordering = ("-rows", "-seats_in_row")

    def save(
        self,
        *,
        force_insert: bool | tuple[models.base.ModelBase, ...] = False,
        force_update: bool = False,
        using: str = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.slug = slugify(self.name)

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self) -> str:
        return f"{self.name} {self.rows}x{self.seats_in_row}"


class Airport(models.Model):
    name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    image = models.ImageField(null=True, upload_to=create_custom_image_path)
    slug = models.SlugField(null=False, default="")

    class Meta:
        ordering = ("country", "city")

    def save(
        self,
        *,
        force_insert: bool | tuple[models.base.ModelBase, ...] = False,
        force_update: bool = False,
        using: str = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.slug = slugify(f"{self.country}-{self.city}-{self.name}")

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self) -> str:
        return f"{self.name} {self.country}/{self.city}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.IntegerField()

    class Meta:
        ordering = ("-distance",)
        constraints = (
            constraints.UniqueConstraint(
                fields=("source", "destination"),
                name="source_destination_unique"
            ),
        )

    def save(
        self,
        *,
        force_insert: bool | tuple[models.base.ModelBase, ...] = False,
        force_update: bool = False,
        using: str = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination} {self.distance} km."


class Crew(models.Model):
    class Role(models.TextChoices):
        COMMANDER = "CN", _("Commander")
        COPILOT = "CP", _("Copilot")
        FLIGHT_ATTENDANT = "FA", _("Flight attendant")

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    role = models.CharField(choices=Role)
    slug = models.SlugField(null=False, default="")

    class Meta:
        verbose_name_plural = "crewmembers"
        ordering = ("role", )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def save(
        self,
        *,
        force_insert: bool | tuple[models.base.ModelBase, ...] = False,
        force_update: bool = False,
        using: str = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.slug = slugify(f"{self.full_name}-{self.role}")

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self) -> str:
        return f"{self.full_name} - {self.get_role_display()}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crewmembers = models.ManyToManyField(Crew, related_name="flights")

    class Meta:
        constraints = (
            constraints.CheckConstraint(
                condition=Q(departure_time__lte=F("arrival_time")),
                name="departure_time_lte_arrival_time"
            ),
        )

    def __str__(self) -> str:
        return (
            f"{self.airplane} "
            f"{self.departure_time.strftime("%Y-%M-%d %H-%m-%S")} -> "
            f"{self.arrival_time.strftime("%Y-%M-%d %H-%m-%S")}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.user} - {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        ordering = ("row", "seat")
        constraints = (
            constraints.UniqueConstraint(
              fields=("row", "seat", "flight"),
                name="row_seat_flight_unique"
            ),
        )

    def clean(self) -> None:
        rows = self.flight.airplane.rows
        seats_in_row = self.flight.airplane.seats_in_row

        if self.row not in range(1, rows + 1):
            raise ValidationError(f"Row must be in range from 1 to {rows}")

        if self.seat not in range(1, seats_in_row + 1):
            raise ValidationError(
                f"Seat must be in range from 1 to {seats_in_row}"
            )

    def __str__(self) -> str:
        return f"Row: {self.row} Seat: {self.seat}"
