from drf_spectacular.openapi import OpenApiResponse

from airport import serializers


GOT_AIRPLANE_TYPES_INFO = OpenApiResponse(
    response=serializers.AirplaneTypeSerializer,
    description="Got all airplane types",
)

GOT_AIRPLANE_TYPE_INFO = OpenApiResponse(
    response=serializers.AirplaneTypeSerializer,
    description="Got airplane type info"
)
