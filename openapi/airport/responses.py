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
    response=serializers.AirplaneSerializer,
    description="Got an airplane info"
)

AIRPLANE_INVALID_DATA = OpenApiResponse(
    description="Invalid data",
    response=OpenApiTypes.OBJECT,
    examples=[
        examples.NAME_IS_BLANK,
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
    status.HTTP_201_CREATED: GOT_AIRPLANE_INFO,
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
    status.HTTP_200_OK: GOT_AIRPLANE_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPLANE_INVALID_DATA,
    status.HTTP_401_UNAUTHORIZED: user_responses.USER_IS_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: user_responses.USER_IS_NOT_ADMIN,
    status.HTTP_404_NOT_FOUND: AIRPLANE_NOT_FOUND,
    status.HTTP_429_TOO_MANY_REQUESTS: user_responses.USER_REACHED_LIMIT_REQUESTS
}

AIRPLANE_PARTIAL_UPDATE_RESPONSES = AIRPLANE_UPDATE_RESPONSES

AIRPLANE_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: None,
    status.HTTP_404_NOT_FOUND: AIRPLANE_NOT_FOUND
}

AIRPLANE_UPLOAD_IMAGE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPLANE_IMAGE_INFO,
    status.HTTP_400_BAD_REQUEST: IMAGE_INVALID_DATA,
    status.HTTP_404_NOT_FOUND: AIRPLANE_NOT_FOUND
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
}

AIRPORT_CREATE_RESPONSES = {
    status.HTTP_201_CREATED: GOT_AIRPORT_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPORT_INVALID_DATA
}

AIRPORT_RETRIEVE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPORT_INFO,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND
}

AIRPORT_UPDATE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPORT_INFO,
    status.HTTP_400_BAD_REQUEST: AIRPORT_INVALID_DATA,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND
}

AIRPORT_PARTIAL_UPDATE_RESPONSES = AIRPORT_UPDATE_RESPONSES

AIRPORT_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: None,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND
}

AIRPORT_UPLOAD_IMAGE_RESPONSES = {
    status.HTTP_200_OK: GOT_AIRPORT_IMAGE_INFO,
    status.HTTP_400_BAD_REQUEST: IMAGE_INVALID_DATA,
    status.HTTP_404_NOT_FOUND: AIRPORT_NOT_FOUND
}

GOT_CREWMEMBERS_INFO = OpenApiResponse(
    description="Got information about crewmembers",
    response=serializers.CrewListRetrieveSerializer
)

CREW_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_CREWMEMBERS_INFO,
    status.HTTP_404_NOT_FOUND: user_responses.PAGE_NOT_FOUND
}
