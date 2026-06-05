from drf_spectacular.openapi import OpenApiResponse

from airport import serializers


GOT_AIRPLANE_TYPES_INFO = OpenApiResponse(
    response=serializers.AirplaneTypeSerializer,
    description="Got all airplane types",
)
