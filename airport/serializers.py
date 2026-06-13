from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import ValidationError

from airport.models import (
    Facility,
    AirplaneType,
    Airplane,
    Airport,
    Crew,
    Route,
    Flight,
    Ticket,
    Order
)


class FacilitySerializer(serializers.ModelSerializer[Facility]):
    class Meta:
        model = Facility
        fields = ("id", "name", "description")


class AirplaneTypeSerializer(serializers.ModelSerializer[AirplaneType]):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer[Airplane]):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "description",
            "airplane_type",
            "rows",
            "seats_in_row",
            "facilities",
            "image"
        )


class AirplaneImageSerializer(AirplaneSerializer):
    image = serializers.ImageField()

    class Meta(AirplaneSerializer.Meta):
        fields = ("id", "image")


class AirplaneListRetrieveSerializer(AirplaneSerializer):
    facilities = serializers.StringRelatedField(many=True)
    airplane_type = serializers.StringRelatedField()


class AirportSerializer(serializers.ModelSerializer[Airport]):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "country",
            "city",
            "description",
            "image",
            "iata_code"
        )


class AirportImageSerializer(AirportSerializer):
    image = serializers.ImageField()

    class Meta(AirportSerializer.Meta):
        fields = ("id", "image")


class CrewSerializer(serializers.ModelSerializer[Crew]):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "role")


class CrewListRetrieveSerializer(CrewSerializer):
    role = serializers.ChoiceField(
        choices=Crew.Role,
        source="get_role_display"
    )


class FlightSerializer(serializers.ModelSerializer[Flight]):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crewmembers"
        )

    def validate(self, attrs: dict) -> dict:
        Flight.validate_departure_time_lte_arrival_time(
            attrs["departure_time"],
            attrs["arrival_time"],
            ValidationError
        )

        return attrs


class FlightListRetrieveSerializer(FlightSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crewmembers = serializers.StringRelatedField(many=True)
    tickets_available = serializers.IntegerField(read_only=True)
    seats_taken = serializers.IntegerField(read_only=True, source="tickets.count")

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + (
            "tickets_available",
            "seats_taken"
        )


class RouteSerializer(serializers.ModelSerializer[Route]):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, attrs: dict) -> dict:
        source = attrs.get("source")
        destination = attrs.get("destination")

        if source is None:
            source = self.instance.source

        if destination is None:
            destination = self.instance.destination

        Route.validate_source_is_different_from_destination(
            source.id,
            destination.id,
            ValidationError
        )

        return attrs


class RouteListRetrieveSerializer(RouteSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()


class TicketSerializer(serializers.ModelSerializer[Ticket]):
    class Meta:
        model = Ticket
        fields = ("id", "flight", "row", "seat")

    def validate(self, attrs: dict) -> dict:
        max_rows = attrs["flight"].airplane.rows
        max_seats = attrs["flight"].airplane.seats_in_row

        Ticket.validate_row_and_seat_in_range(
            attrs["row"],
            attrs["seat"],
            max_rows,
            max_seats,
            ValidationError
        )
        return attrs


class OrderSerializer(serializers.ModelSerializer[Order]):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets")

    def create(self, validated_data: dict) -> Order:
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)

            for ticket_data in tickets_data:
                Ticket.objects.create(**ticket_data, order_id=order.id)

        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        with transaction.atomic():
            tickets_data = self.initial_data.pop("tickets")

            for ticket_data in tickets_data:
                if ticket_data.get("id") is None:
                    Ticket.objects.create(
                        flight_id=ticket_data["flight"],
                        row=ticket_data["row"],
                        seat=ticket_data["seat"],
                        order_id=instance.id
                    )
                else:
                    ticket_id = ticket_data.pop("id")
                    instance.tickets.filter(id=ticket_id).update(
                        **ticket_data
                    )

        return instance


class OrderListRetrieveSerializer(OrderSerializer):
    tickets = serializers.StringRelatedField(many=True)
