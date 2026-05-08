from rest_framework import serializers

from airport.models import Facility


class FacilitySerializer(serializers.ModelSerializer[Facility]):
    class Meta:
        model = Facility
        fields = "__all__"
