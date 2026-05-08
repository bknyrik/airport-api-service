from rest_framework.viewsets import ModelViewSet

from airport.models import (
    Facility,
    AirplaneType,
    Airplane
)
from airport.serializers import (
    FacilitySerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer
)


class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.prefetch_related("facilities")
    serializer_class = AirplaneSerializer
