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
from airport.pagination import (
    AirplanePagination,
    AirportSetPagination,
    CrewSetPagination
)


class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = serializers.FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = serializers.AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.prefetch_related("facilities")
    pagination_class = AirplanePagination

    def get_queryset(self) -> QuerySet[Airplane]:
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("airplane_type")

            facilities_ids = self.request.query_params.get("facilities_ids")
            airplane_type = self.request.query_params.get("airplane_type")

            if facilities_ids:
                queryset = queryset.filter(
                    facilities__in=tuple(map(int, facilities_ids.split(",")))
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
    pagination_class = AirportSetPagination

    def get_queryset(self) -> QuerySet[Airport]:
        queryset = Airport.objects.all()

        if self.action == "list":
            country = self.request.query_params.get("country")
            city = self.request.query_params.get("city")
            iata_code = self.request.query_params.get("iata_code")

            if country:
                queryset = queryset.filter(country__iexact=country)

            if city:
                queryset = queryset.filter(city__iexact=city)

            if iata_code:
                queryset = queryset.filter(iata_code__icontains=iata_code)

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
    pagination_class = CrewSetPagination

    def get_queryset(self) -> QuerySet[Crew]:
        queryset = Crew.objects.all()

        if self.action == "list":
            first_name = self.request.query_params.get("first_name")
            last_name= self.request.query_params.get("last_name")
            role = self.request.query_params.get("role")

            if first_name:
                queryset = queryset.filter(first_name__icontains=first_name)

            if last_name:
                queryset = queryset.filter(last_name__icontains=last_name)

            if role:
                queryset = queryset.filter(
                    role__iexact=role
                )

        return queryset

    def get_serializer_class(self) -> type[serializers.CrewSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.CrewListRetrieveSerializer

        return serializers.CrewSerializer


class RouteViewSet(ModelViewSet):

    def get_queryset(self) -> QuerySet[Route]:
        queryset = Route.objects.select_related("source", "destination")

        if self.action == "list":
            source_id = self.request.query_params.get("source_id")
            destination_id = self.request.query_params.get("destination_id")
            min_distance = self.request.query_params.get("min_distance")
            max_distance = self.request.query_params.get("max_distance")

            if source_id:
                queryset = queryset.filter(source_id=source_id)

            if destination_id:
                queryset = queryset.filter(destination_id=destination_id)

            if min_distance:
                queryset = queryset.filter(distance__gte=min_distance)

            if max_distance:
                queryset = queryset.filter(distance__lte=max_distance)

        return queryset

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

        if self.action == "list":
            airplane_id = self.request.query_params.get("airplane_id")
            route_id = self.request.query_params.get("route_id")
            crewmembers_ids = self.request.query_params.get("crewmembers_ids")

            if airplane_id:
                queryset = queryset.filter(airplane_id=airplane_id)

            if route_id:
                queryset = queryset.filter(route_id=route_id)

            if crewmembers_ids:
                queryset = queryset.filter(
                    crewmembers__in=tuple(
                         map(int, crewmembers_ids.split(","))
                    )
                ).distinct()

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
