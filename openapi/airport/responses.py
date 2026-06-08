from rest_framework import status
from drf_spectacular.openapi import OpenApiResponse, OpenApiTypes

from airport import serializers
from openapi.airport import examples
from openapi.user import responses as user_responses


GOT_AIRPLANE_TYPES_INFO = OpenApiResponse(
    response=serializers.AirplaneTypeSerializer,
    description="Got all airplane types",
)

GOT_AIRPLANE_TYPE_INFO = OpenApiResponse(
    response=serializers.AirplaneTypeSerializer,
    description="Got airplane type info"
)

AIRPLANE_TYPE_NOT_FOUND = OpenApiResponse(
    response={
        "example": {
          "detail": "No AirplaneType matches the given query."
        }
    },
    description="Airplane type not found"
)

AIRPLANE_TYPE_INVALID_DATA = OpenApiResponse(
    description="Invalid input data",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.AIRPLANE_TYPE_NAME_EXISTS,
        examples.NAME_IS_BLANK,
        examples.NAME_HAS_INVALID_LENGTH
    ]
)

AIRPLANE_TYPE_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPLANE_TYPES_INFO,
    status.HTTP_404_NOT_FOUND: user_responses.PAGE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_TYPE_RETRIEVE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPLANE_TYPE_INFO,
    status.HTTP_404_NOT_FOUND: AIRPLANE_TYPE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: (
        user_responses.USER_REACHED_LIMIT_REQUESTS
    )
}

AIRPLANE_TYPE_CREATE_RESPONSES = {
    status.HTTP_201_CREATED: GOT_AIRPLANE_TYPE_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPLANE_TYPE_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_TYPE_UPDATE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPLANE_TYPE_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPLANE_TYPE_INVALID_DATA,
    status.HTTP_404_NOT_FOUND: AIRPLANE_TYPE_NOT_FOUND,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_TYPE_PARTIAL_UPDATE_RESPONSES = AIRPLANE_TYPE_UPDATE_RESPONSES

AIRPLANE_TYPE_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: None,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: AIRPLANE_TYPE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

GOT_AIRPLANES_INFO = OpenApiResponse(
    response=serializers.AirplaneListRetrieveSerializer,
    description="Got airplanes"
)

AIRPLANE_LIST_INVALID_PARAMS = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Invalid parameters",
    examples=[
        examples.AIRPLANE_TYPE_ID_INVALID_CHOICE,
        examples.FACILITIES_INVALID_CHOICE,
    ]
)

GOT_AIRPLANE_INFO = OpenApiResponse(
    response=serializers.AirplaneListRetrieveSerializer,
    description="Got an airplane info"
)

GOT_DETAILED_AIRPLANE_INFO = OpenApiResponse(
    description="Got detailed information about airplane",
    response=serializers.AirplaneSerializer
)

AIRPLANE_INVALID_DATA = OpenApiResponse(
    description="Invalid data",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.NAME_IS_BLANK,
        examples.NAME_HAS_INVALID_LENGTH,
        examples.AIRPLANE_TYPE_INVALID_PK,
        examples.FACILITIES_INVALID_PK,
        examples.ROWS_LESS_THAN_ONE,
        examples.SEATS_IN_ROW_LESS_THAN_ONE
    ]
)

AIRPLANE_NOT_FOUND = OpenApiResponse(
    description="Airplane not found",
    response={"example": {"detail": "No Airplane matches the given query."}}
)

GOT_AIRPLANE_IMAGE_INFO = OpenApiResponse(
    description="Got the image of the airplane",
    response=serializers.AirplaneImageSerializer
)

IMAGE_INVALID_DATA = OpenApiResponse(
    description="Invalid input data",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.IMAGE_WAS_NOT_A_FILE,
        examples.IMAGE_IS_NOT_VALID
    ]
)

AIRPLANE_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPLANES_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPLANE_LIST_INVALID_PARAMS,
    status.HTTP_404_NOT_FOUND: user_responses.PAGE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_CREATE_RESPONSES = {
    status.HTTP_201_CREATED: GOT_DETAILED_AIRPLANE_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPLANE_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_RETRIEVE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPLANE_INFO,
    status.HTTP_404_NOT_FOUND: AIRPLANE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_UPDATE_RESPONSES = {
    status.HTTP_200_OK: GOT_DETAILED_AIRPLANE_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPLANE_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: AIRPLANE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_PARTIAL_UPDATE_RESPONSES = AIRPLANE_UPDATE_RESPONSES

AIRPLANE_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: None,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: AIRPLANE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_UPLOAD_IMAGE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPLANE_IMAGE_INFO,
    status.HTTP_400_BAD_REQUEST: IMAGE_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: AIRPLANE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

GOT_AIRPORTS_INFO = OpenApiResponse(
    description="Got info about airports",
    response=serializers.AirportSerializer
)

GOT_AIRPORT_INFO = OpenApiResponse(
    description="Got info about airport",
    response=serializers.AirportSerializer
)

AIRPORT_INVALID_DATA = OpenApiResponse(
    description="Invalid input data",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.NAME_IS_BLANK,
        examples.COUNTRY_IS_BLANK,
        examples.CITY_IS_BLANK,
        examples.AIRPORT_EXISTS,
        examples.AIRPORT_IATA_CODE_IS_INVALID
    ]
)

AIRPORT_NOT_FOUND = OpenApiResponse(
    description="Airport not found",
    response={"example": {"detail": "No Airport matches the given query."}}
)


GOT_AIRPORT_IMAGE_INFO = OpenApiResponse(
    description="Got the image of the airport",
    response=serializers.AirportImageSerializer
)

AIRPORT_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPORTS_INFO,
    status.HTTP_404_NOT_FOUND: user_responses.PAGE_NOT_FOUND,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPORT_CREATE_RESPONSES = {
    status.HTTP_201_CREATED: GOT_AIRPORT_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPORT_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPORT_RETRIEVE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPORT_INFO,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPORT_UPDATE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPORT_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPORT_INVALID_DATA,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPORT_PARTIAL_UPDATE_RESPONSES = AIRPORT_UPDATE_RESPONSES

AIRPORT_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: None,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPORT_UPLOAD_IMAGE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPORT_IMAGE_INFO,
    status.HTTP_400_BAD_REQUEST: IMAGE_INVALID_DATA,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

GOT_CREWMEMBERS_INFO = OpenApiResponse(
    description="Got information about crewmembers",
    response=serializers.CrewListRetrieveSerializer
)

GOT_CREW_INFO = OpenApiResponse(
    description="Got information about crewmember",
    response=serializers.CrewListRetrieveSerializer
)

GOT_DETAILED_CREW_INFO = OpenApiResponse(
    description="Got detailed information about crewmember",
    response=serializers.CrewSerializer
)

CREW_NOT_FOUND = OpenApiResponse(
    description="Crew not found",
    response={"example": {"detail": "No Crew matches the given query."}}
)

CREW_INVALID_DATA = OpenApiResponse(
    description="Invalid input data",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.FIRST_NAME_IS_BLANK,
        examples.FIRST_NAME_HAS_INVALID_LENGTH,
        examples.LAST_NAME_IS_BLANK,
        examples.LAST_NAME_HAS_INVALID_LENGTH,
        examples.ROLE_INVALID_CHOICE
    ]
)

CREW_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_CREWMEMBERS_INFO,
    status.HTTP_404_NOT_FOUND: user_responses.PAGE_NOT_FOUND,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

CREW_CREATE_RESPONSES = {
    status.HTTP_201_CREATED: GOT_DETAILED_CREW_INFO,
    status.HTTP_400_BAD_REQUEST: CREW_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

CREW_RETRIEVE_RESPONSES = {
    status.HTTP_200_OK: GOT_CREW_INFO,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: CREW_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

CREW_UPDATE_RESPONSES = {
    status.HTTP_200_OK: GOT_DETAILED_CREW_INFO,
    status.HTTP_400_BAD_REQUEST: CREW_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: CREW_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

CREW_PARTIAL_UPDATE_RESPONSES = CREW_UPDATE_RESPONSES

CREW_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: None,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: CREW_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

GOT_FACILITIES_INFO = OpenApiResponse(
    description="Got information about facilities",
    response=serializers.FacilitySerializer
)

GOT_FACILITY_INFO = OpenApiResponse(
    description="Got information about facility",
    response=serializers.FacilitySerializer
)

FACILITY_INVALID_DATA = OpenApiResponse(
    description="Invalid input data",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.NAME_IS_BLANK,
        examples.FACILITY_NAME_EXISTS
    ]
)

FACILITY_NOT_FOUND = OpenApiResponse(
    description="Facility not found",
    response={"example": {"detail": "No Facility matches the given query."}}
)

FACILITY_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_FACILITIES_INFO,
    status.HTTP_404_NOT_FOUND: user_responses.PAGE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

FACILITY_CREATE_RESPONSES = {
    status.HTTP_201_CREATED: GOT_FACILITY_INFO,
    status.HTTP_400_BAD_REQUEST: FACILITY_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

FACILITY_RETRIEVE_RESPONSES = {
    status.HTTP_200_OK: GOT_FACILITY_INFO,
    status.HTTP_404_NOT_FOUND: FACILITY_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

FACILITY_UPDATE_RESPONSES = {
    status.HTTP_200_OK: GOT_FACILITY_INFO,
    status.HTTP_400_BAD_REQUEST: FACILITY_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_404_NOT_FOUND: FACILITY_NOT_FOUND,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

FACILITY_PARTIAL_UPDATE_RESPONSES = FACILITY_UPDATE_RESPONSES

FACILITY_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: None,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_404_NOT_FOUND: FACILITY_NOT_FOUND,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

GOT_FLIGHTS_INFO = OpenApiResponse(
    description="Got information about flights",
    response=serializers.FlightListRetrieveSerializer
)

GOT_FLIGHT_INFO = OpenApiResponse(
    description="Got information about flight",
    response=serializers.FlightListRetrieveSerializer
)

FLIGHT_NOT_FOUND = OpenApiResponse(
    description="Flight not found",
    response={"example": {"detail": "No Flight matches the given query."}}
)

FLIGHT_LIST_INVALID_PARAMETERS = OpenApiResponse(
    description="Invalid parameters",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.AIRPLANE_ID_INVALID_CHOICE,
        examples.ROUTE_ID_INVALID_CHOICE,
        examples.CREWMEMBERS_INVALID_CHOICE
    ]
)

FLIGHT_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_FLIGHTS_INFO,
    status.HTTP_400_BAD_REQUEST: FLIGHT_LIST_INVALID_PARAMETERS,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}
