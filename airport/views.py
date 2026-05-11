from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from airport.models import (
    Facility,
    AirplaneType,
    Airplane,
    Airport,
    Crew,
    Route
)
from airport.serializers import (
    FacilitySerializer,
    FacilityListSerializer,
    AirplaneTypeSerializer,
    AirplaneTypeListSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    AirplaneImageSerializer,
    AirportSerializer,
    AirportListSerializer,
    AirportImageSerializer,
    CrewSerializer,
    CrewListSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer
)


class FacilityViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = Facility.objects.all()

    def get_serializer_class(self) -> type[FacilitySerializer]:
        if self.action == "list":
            return FacilityListSerializer

        return FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = AirplaneType.objects.all()

    def get_serializer_class(self) -> type[AirplaneTypeSerializer]:
        if self.action == "list":
            return AirplaneTypeListSerializer

        return AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = Airplane.objects.prefetch_related("facilities")

    def get_queryset(self) -> QuerySet[Airplane]:
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("airplane_type")

        return queryset

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
    def upload_image(self, request: Request, slug: str = None) -> Response:
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AirportViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = Airport.objects.all()

    def get_serializer_class(self) -> type[AirportSerializer]:
        if self.action == "list":
            return AirportListSerializer

        if self.action == "upload_image":
            return AirportImageSerializer

        return AirportSerializer

    @action(
        methods=("POST",),
        detail=True,
        url_path="upload_image"
    )
    def upload_image(self, request: Request, slug: str = None) -> Response:
        airport = self.get_object()
        serializer = self.get_serializer(airport, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CrewViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = Crew.objects.all()

    def get_serializer_class(self) -> type[CrewSerializer]:
        if self.action == "list":
            return CrewListSerializer

        return CrewSerializer


class RouteViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self) -> type[RouteSerializer]:
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteRetrieveSerializer

        return RouteSerializer
