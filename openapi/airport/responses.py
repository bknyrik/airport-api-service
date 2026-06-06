from drf_spectacular.openapi import OpenApiResponse, OpenApiTypes

from airport import serializers
from openapi.airport import examples


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
