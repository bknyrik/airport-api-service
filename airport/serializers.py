from rest_framework import serializers

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


class AirplaneListSerializer(AirplaneSerializer):
    facilities = serializers.StringRelatedField(many=True)
    airplane_type = serializers.StringRelatedField()


class AirplaneRetrieveSerializer(AirplaneSerializer):
    facilities = FacilityListSerializer(many=True)
    airplane_type = AirplaneTypeSerializer()


class AirportSerializer(serializers.ModelSerializer[Airport]):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "country", "city", "description", "image")


class AirportImageSerializer(AirportSerializer):
    image = serializers.ImageField()

    class Meta(AirportSerializer.Meta):
        fields = ("id", "image")


class AirportListSerializer(AirportSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:airport-detail",
        lookup_field="slug"
    )

    class Meta(AirportSerializer.Meta):
        fields = ("url", ) + AirportSerializer.Meta.fields


class CrewSerializer(serializers.ModelSerializer[Crew]):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "role")


class CrewListSerializer(CrewSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:crew-detail",
        lookup_field="slug"
    )
    role = serializers.ChoiceField(
        choices=Crew.Role,
        source="get_role_display"
    )

    class Meta(CrewSerializer.Meta):
        fields = ("url", ) + CrewSerializer.Meta.fields


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


class FlightListSerializer(FlightSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:flight-detail"
    )
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crewmembers = serializers.StringRelatedField(many=True)

    class Meta(FlightSerializer.Meta):
        fields = ("url", ) + FlightSerializer.Meta.fields


class RouteSerializer(serializers.ModelSerializer[Route]):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:route-detail",
    )
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta(RouteSerializer.Meta):
        fields = ("url", ) + RouteSerializer.Meta.fields


class RouteRetrieveSerializer(RouteSerializer):
    source = AirportListSerializer()
    destination = AirportListSerializer()


class FlightRetrieveSerializer(FlightSerializer):
    route = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="airport:route-detail",
    )
    airplane = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="airport:airplane-detail",
        lookup_field="slug"
    )
    crewmembers = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="airport:crew-detail",
        lookup_field="slug"
    )


class TicketSerializer(serializers.ModelSerializer[Ticket]):
    class Meta:
        model = Ticket
        fields = ("id", "flight", "row", "seat")


class OrderSerializer(serializers.ModelSerializer[Order]):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets")


class OrderListSerializer(OrderSerializer):
    tickets = serializers.StringRelatedField(many=True)
