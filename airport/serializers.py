from rest_framework import serializers

from airport.models import (
    Facility,
    AirplaneType,
    Airplane,
    Airport,
    Crew
)


class FacilitySerializer(serializers.ModelSerializer[Facility]):
    class Meta:
        model = Facility
        fields = "__all__"


class AirplaneTypeSerializer(serializers.ModelSerializer[AirplaneType]):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer[Airplane]):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
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
    facilities = FacilitySerializer(many=True)
    airplane_type = AirplaneTypeSerializer()


class AirportSerializer(serializers.ModelSerializer[Airport]):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "country", "city", "image")


class AirportImageSerializer(AirportSerializer):
    image = serializers.ImageField()

    class Meta(AirportSerializer.Meta):
        fields = ("id", "image")


class CrewSerializer(serializers.ModelSerializer[Crew]):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "role")


class CrewListSerializer(CrewSerializer):
    role = serializers.ChoiceField(
        choices=Crew.Role,
        source="get_role_display"
    )
