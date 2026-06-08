from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes

from airport.models import Crew


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

AIRPORT_LIST_PARAMETERS = [COUNTRY, CITY, IATA_CODE]

CREW_FIRST_NAME = OpenApiParameter(
    name="first_name",
    type=str,
    description="Filter by characters in first name"
)

CREW_LAST_NAME = OpenApiParameter(
    name="last_name",
    type=str,
    description="Filter by characters in last name"
)

CREW_ROLE = OpenApiParameter(
    name="role",
    enum=Crew.Role,
    description="Filter by role from the given values"
)

CREW_LIST_PARAMETERS = [
    CREW_FIRST_NAME,
    CREW_LAST_NAME,
    CREW_ROLE
]

AIRPLANE_ID = OpenApiParameter(
    name="airplane_id",
    type=int,
    description="Filter by airplane id"
)

CREWMEMBERS_IDS = OpenApiParameter(
    name="crewmembers",
    type={"type": "array", "items": {"type": "number"}},
    description="Filter by crewmembers ids"
)

ROUTE_ID = OpenApiParameter(
    name="route_id",
    type=int,
    description="Filter by route id"
)

FLIGHT_LIST_PARAMETERS = [
    AIRPLANE_ID,
    CREWMEMBERS_IDS,
    ROUTE_ID
]

SOURCE_ID = OpenApiParameter(
    name="source_id",
    type=int,
    description="Filter by source id"
)

DESTINATION_ID = OpenApiParameter(
    name="source_id",
    type=int,
    description="Filter by source id"
)

MIN_DISTANCE = OpenApiParameter(
    name="min_distance",
    type=int,
    description="Filter by min distance"
)

MAX_DISTANCE = OpenApiParameter(
    name="max_distance",
    type=int,
    description="Filter by max distance"
)

ROUTE_LIST_PARAMETERS = [
    SOURCE_ID,
    DESTINATION_ID,
    MIN_DISTANCE,
    MAX_DISTANCE
]
