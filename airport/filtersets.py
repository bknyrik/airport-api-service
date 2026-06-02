from django_filters.rest_framework import FilterSet
from django_filters import filters

from airport.models import Airport


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
