from rest_framework import serializers

from airport.models import (
    Facility,
    AirplaneType,
    Airplane
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
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane_type",
            "rows",
            "seats_in_row",
            "facilities",
            "image",
        )


class AirplaneListSerializer(AirplaneSerializer):
    facilities = serializers.StringRelatedField(many=True)
    airplane_type = serializers.StringRelatedField()


class AirplaneRetrieveSerializer(AirplaneSerializer):
    facilities = FacilitySerializer(many=True)
    airplane_type = AirplaneTypeSerializer()
