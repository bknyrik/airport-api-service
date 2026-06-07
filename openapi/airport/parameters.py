from drf_spectacular.openapi import OpenApiParameter


AIRPLANE_TYPE_ID = OpenApiParameter(
    name="airplane_type_id",
    type=int,
    description="Filter by id of airplane type"
)

FACILITIES_IDS = OpenApiParameter(
    name="facilities",
    type={"type": "array", "items": {"type": "number"}},
    description="Filter by ids of facilities"
)

AIRPLANE_LIST_PARAMETERS = [
    AIRPLANE_TYPE_ID,
    FACILITIES_IDS
]

COUNTRY = OpenApiParameter(
    name="country",
    type=str,
    description="Filter by country"
)

CITY = OpenApiParameter(
    name="city",
    type=str,
    description="Filter by city"
)

IATA_CODE = OpenApiParameter(
    name="iata_code",
    type=str,
    description="Filter by characters in IATA code"
)
