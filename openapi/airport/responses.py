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
    status.HTTP_401_UNAUTHORIZED: (
        user_responses.USER_IS_NOT_AUTHORIZED
    ),
    status.HTTP_429_TOO_MANY_REQUESTS: (
        user_responses.REQUEST_IS_THROTTLED
    )
}
