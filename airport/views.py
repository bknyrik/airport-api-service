from rest_framework.viewsets import ModelViewSet

from airport.models import (
    Facility,
    AirplaneType,
    Airplane
)
from airport.serializers import (
    FacilitySerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer
)


class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.prefetch_related("facilities")

    def get_serializer_class(self) -> type[AirplaneSerializer]:
        if self.action == "list":
            return AirplaneListSerializer

        if self.action == "retrieve":
            return AirplaneRetrieveSerializer

        return AirplaneSerializer
