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
    image = serializers.ImageField(required=True)

    class Meta(AirplaneSerializer.Meta):
        fields = ("id", "image")


class AirplaneListRetrieveSerializer(AirplaneSerializer):
    facilities = serializers.StringRelatedField(many=True)
    airplane_type = serializers.StringRelatedField()


class AirportSerializer(serializers.ModelSerializer[Airport]):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "country", "city", "description", "image")


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


class FlightListRetrieveSerializer(FlightSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crewmembers = serializers.StringRelatedField(many=True)


class RouteSerializer(serializers.ModelSerializer[Route]):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


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

        Ticket.validate_row_and_seat(
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


class OrderListSerializer(OrderSerializer):
    tickets = serializers.StringRelatedField(many=True)
