from django.db.models import QuerySet, F, Count
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

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
from airport import pagination
from airport import filtersets
from openapi.airport import responses as airport_responses
from openapi.user import responses as user_responses


class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = serializers.FacilitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = serializers.AirplaneTypeSerializer

    @extend_schema(
        description="Returns list with all airplane types.",
        summary="Get all airplane types",
        responses={
            status.HTTP_200_OK: airport_responses.GOT_AIRPLANE_TYPES_INFO,
            status.HTTP_401_UNAUTHORIZED: (
                user_responses.USER_IS_NOT_AUTHORIZED
            ),
            status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
            status.HTTP_429_TOO_MANY_REQUESTS: (
                user_responses.REQUEST_IS_THROTTLED
            )
        }
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Returns information about airplane type by id.",
        summary="Get airplane type by id",
        responses={
            status.HTTP_200_OK: airport_responses.GOT_AIRPLANE_TYPES_INFO,
            status.HTTP_401_UNAUTHORIZED: (
                user_responses.USER_IS_NOT_AUTHORIZED
            ),
            status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
            status.HTTP_404_NOT_FOUND: (
                airport_responses.AIRPLANE_TYPE_NOT_FOUND
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: (
                user_responses.REQUEST_IS_THROTTLED
            )
        }
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.prefetch_related("facilities")
    pagination_class = pagination.AirplaneSetPagination
    filterset_fields = ("airplane_type_id", "facilities")

    def get_queryset(self) -> QuerySet[Airplane]:
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("airplane_type")

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
    pagination_class = pagination.AirportSetPagination
    filterset_class = filtersets.AirportFilterSet

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
    pagination_class = pagination.CrewSetPagination
    filterset_class = filtersets.CrewFilterSet

    def get_serializer_class(self) -> type[serializers.CrewSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.CrewListRetrieveSerializer

        return serializers.CrewSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    pagination_class = pagination.RouteSetPagination
    filterset_class = filtersets.RouteFilterSet

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
    pagination_class = pagination.FlightSetPagination
    filterset_fields = ("airplane_id", "route_id", "crewmembers")

    def get_queryset(self) -> QuerySet[Flight]:
        return self.queryset.annotate(
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
    pagination_class = pagination.OrderSetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self) -> type[serializers.OrderSerializer]:
        if self.action in ("list", "retrieve"):
            return serializers.OrderListRetrieveSerializer

        return serializers.OrderSerializer

    def perform_create(self, serializer: serializers.OrderSerializer) -> None:
        serializer.save(user=self.request.user)
