from django.db import models
from django.db.models import constraints
from django.conf import settings


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

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)

    class Meta:
        ordering = ("name", )
        constraints = (
            constraints.UniqueConstraint(
                fields=("country", "city"),
                name="unique_country_city"
            ),
        )

    def __str__(self) -> str:
        return "%s %s/%s" % (self.name, self.country, self.city)


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    distance = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.source}-{self.destination} {self.distance}"


class Crew(models.Model):
    POSITION_CHOICES = (
        ("PL", "Pilot"),
        ("FA", "Flight attendant"),
        ("FE", "Flight engineer"),
        ("NG", "Navigator"),
        ("RO", "Radio operator")
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    position = models.CharField(choices=POSITION_CHOICES)

    @property
    def full_name(self) -> str:
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self) -> str:
        return f"%s - %s" % (self.full_name, self.get_position_display())


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
        ordering = ("created_at",)

    def __str__(self) -> str:
        return str(self.created_at)
