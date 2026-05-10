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
        fields = ("id", "name", "description")


class FacilityListSerializer(FacilitySerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:facility-detail",
        lookup_field="slug"
    )

    class Meta(FacilitySerializer.Meta):
        fields = ("url", ) + FacilitySerializer.Meta.fields


class AirplaneTypeSerializer(serializers.ModelSerializer[AirplaneType]):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneTypeListSerializer(AirplaneTypeSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:airplanetype-detail",
        lookup_field="slug"
    )

    class Meta(AirplaneTypeSerializer.Meta):
        fields = ("url", ) + AirplaneTypeSerializer.Meta.fields


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
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:airplane-detail",
        lookup_field="slug"
    )
    facilities = serializers.StringRelatedField(many=True)
    airplane_type = serializers.StringRelatedField()

    class Meta(AirplaneSerializer.Meta):
        fields = ("url", ) + AirplaneSerializer.Meta.fields


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
    role = serializers.ChoiceField(
        choices=Crew.Role,
        source="get_role_display"
    )
