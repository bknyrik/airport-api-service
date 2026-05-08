from rest_framework import serializers

from airport.models import (
    Facility,
    AirplaneType
)


class FacilitySerializer(serializers.ModelSerializer[Facility]):
    class Meta:
        model = Facility
        fields = "__all__"


class AirplaneTypeSerializer(serializers.ModelSerializer[AirplaneType]):
    class Meta:
        model = AirplaneType
        field = "__all__"
