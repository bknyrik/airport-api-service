from django.db.models import QuerySet, F, Count
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
    queryset = Facility.objects.all()
    serializer_class = serializers.FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = serializers.AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.prefetch_related("facilities")

    def get_queryset(self) -> QuerySet[Airplane]:
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("airplane_type")

            facilities = self.request.query_params.get("facilities")
            airplane_type = self.request.query_params.get("airplane_type")

            if facilities:
                facilities = tuple(map(int, facilities.split(",")))
                queryset = queryset.filter(
                    facilities__in=facilities
                ).distinct()

            if airplane_type:
                queryset = queryset.filter(
                    airplane_type__name__iexact=airplane_type
                )

        return queryset

    def get_serializer_class(self) -> type[serializers.AirplaneSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.AirplaneListRetrieveSerializer

        if self.action == "upload_image":
            return serializers.AirplaneImageSerializer

        return serializers.AirplaneSerializer

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


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()

    def get_queryset(self) -> QuerySet[Airport]:
        queryset = self.queryset

        if self.action == "list":
            country = self.request.query_params.get("country")
            city = self.request.query_params.get("city")

            if country:
                queryset = queryset.filter(country__iexact=country)

            if city:
                queryset = queryset.filter(city__iexact=city)

        return queryset

    def get_serializer_class(self) -> type[serializers.AirportSerializer]:
        if self.action == "upload_image":
            return serializers.AirportImageSerializer

        return serializers.AirportSerializer

    @action(
        methods=("POST",),
        detail=True,
        url_path="upload_image"
    )
    def upload_image(self, request: Request, pk: int = None) -> Response:
        airport = self.get_object()
        serializer = self.get_serializer(airport, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()

    def get_serializer_class(self) -> type[serializers.CrewSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.CrewListRetrieveSerializer

        return serializers.CrewSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self) -> type[serializers.RouteSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.RouteListRetrieveSerializer

        return serializers.RouteSerializer


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.prefetch_related(
        "crewmembers",
        "tickets"
    ).select_related(
        "airplane",
        "route__source",
        "route__destination"
    )

    def get_queryset(self) -> QuerySet[Flight]:
        queryset = self.queryset

        return queryset.annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )

    def get_serializer_class(self) -> type[serializers.FlightSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.FlightListRetrieveSerializer

        return serializers.FlightSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("tickets")

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self) -> type[serializers.OrderSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.OrderListRetrieveSerializer

        return serializers.OrderSerializer

    def perform_create(self, serializer: serializers.OrderSerializer) -> None:
        serializer.save(user=self.request.user)
