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
    Route,
    Flight,
    Order
)
from airport import serializers


class FacilityViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = Facility.objects.all()

    def get_serializer_class(self) -> type[serializers.FacilitySerializer]:
        if self.action == "list":
            return serializers.FacilityListSerializer

        return serializers.FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = AirplaneType.objects.all()

    def get_serializer_class(
        self
    ) -> type[serializers.AirplaneTypeSerializer]:
        if self.action == "list":
            return serializers.AirplaneTypeListSerializer

        return serializers.AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.prefetch_related("facilities")

    def get_queryset(self) -> QuerySet[Airplane]:
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("airplane_type")

        return queryset

    def get_serializer_class(self) -> type[serializers.AirplaneSerializer]:
        if self.action == "list":
            return serializers.AirplaneListSerializer

        if self.action == "retrieve":
            return serializers.AirplaneRetrieveSerializer

        if self.action == "upload_image":
            return serializers.AirplaneImageSerializer

        return serializers.AirplaneSerializer

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

    def get_serializer_class(self) -> type[serializers.AirportSerializer]:
        if self.action == "list":
            return serializers.AirportListSerializer

        if self.action == "upload_image":
            return serializers.AirportImageSerializer

        return serializers.AirportSerializer

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

    def get_serializer_class(self) -> type[serializers.CrewSerializer]:
        if self.action == "list":
            return serializers.CrewListSerializer

        return serializers.CrewSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self) -> type[serializers.RouteSerializer]:
        if self.action == "list":
            return serializers.RouteListSerializer

        if self.action == "retrieve":
            return serializers.RouteRetrieveSerializer

        return serializers.RouteSerializer


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.prefetch_related("crewmembers")

    def get_queryset(self) -> QuerySet[Flight]:
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related(
                "airplane",
                "route__source",
                "route__destination"
            )

        return queryset

    def get_serializer_class(self) -> type[serializers.FlightSerializer]:
        if self.action == "list":
            return serializers.FlightListSerializer

        elif self.action == "retrieve":
            return serializers.FlightRetrieveSerializer

        return serializers.FlightSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self) -> type[serializers.OrderSerializer]:
        if self.action == "list":
            return serializers.OrderListSerializer

        return serializers.OrderSerializer
