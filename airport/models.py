from __future__ import annotations
import os
import uuid

from django.db import models
from django.db.models import constraints
from django.db.models import Q, F
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.text import slugify


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
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = "facilities"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=64)
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

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    image = models.ImageField(null=True, upload_to=create_custom_image_path)

    class Meta:
        ordering = ("country", "city")

    def __str__(self) -> str:
        return "%s %s/%s" % (self.name, self.country, self.city)


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

    def __str__(self) -> str:
        return f"{self.source}-{self.destination} {self.distance}"


class Crew(models.Model):
    class Role(models.TextChoices):
        COMMANDER = "CN", _("Commander")
        COPILOT = "CP", _("Copilot")
        FLIGHT_ATTENDANT = "FA", _("Flight attendant")

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    role = models.CharField(choices=Role)

    class Meta:
        verbose_name_plural = "crewmembers"
        ordering = ("role", )

    @property
    def full_name(self) -> str:
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self) -> str:
        return f"%s - %s" % (self.full_name, self.get_role_display())


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
            constraints.UniqueConstraint(
                fields=("route", "airplane"),
                name="route_airplane_unique"
            ),
            constraints.CheckConstraint(
                condition=Q(departure_time__lte=F("arrival_time")),
                name="departure_time_lte_arrival_time"
            ),
        )

    def __str__(self) -> str:
        return f"%s %s-%s" % (
            self.route,
            self.departure_time,
            self.arrival_time
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
        return str(self.created_at)


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
        constraints = (
            constraints.CheckConstraint(
                condition=Q(row__range=(1, F("flight__airplane__row"))),
                name="row_range_flight_airplane_row"
            ),
            constraints.CheckConstraint(
                condition=Q(seat__range=(1, F("flight__airplane__seats_in_row"))),
                name="seat_range_flight_airplane_seats_in_row"
            )
        )

    def __str__(self) -> str:
        return "Row: %d Seat: %d" % (self.row, self.seat)
