from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

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
    AirplaneRetrieveSerializer,
    AirplaneImageSerializer
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

        if self.action == "upload_image":
            return AirplaneImageSerializer

        return AirplaneSerializer

    @action(
        methods=("POST",),
        detail=True,
        url_path="upload_image",
    )
    def upload_image(self, request: Request, pk: int = None) -> Response:
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
