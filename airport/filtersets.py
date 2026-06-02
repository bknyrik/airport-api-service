from django_filters.rest_framework import FilterSet
from django_filters import filters

from airport.models import Airport, Crew, Route


class AirportFilterSet(FilterSet):
    class Meta:
        model = Airport
        fields = ("country", "city", "iata_code")

    country = filters.CharFilter(
        field_name="country",
        lookup_expr="iexact"
    )
    city = filters.CharFilter(
        field_name="city",
        lookup_expr="iexact"
    )
    iata_code = filters.CharFilter(
        field_name="iata_code",
        lookup_expr="icontains"
    )


class CrewFilterSet(FilterSet):
    class Meta:
        model = Crew
        fields = ("first_name", "last_name", "role")

    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains"
    )


class RouteFilterSet(FilterSet):
    class Meta:
        model = Route
        fields = (
            "source_id",
            "destination_id",
            "min_distance",
            "max_distance",
        )

    min_distance = filters.NumberFilter(
        field_name="distance",
        lookup_expr="gte"
    )
    max_distance = filters.NumberFilter(
        field_name="distance",
        lookup_expr="gte"
    )
