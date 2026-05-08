from rest_framework.viewsets import ModelViewSet

from airport.models import (
    Facility,
    AirplaneType
)
from airport.serializers import (
    FacilitySerializer,
    AirplaneTypeSerializer
)


class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
