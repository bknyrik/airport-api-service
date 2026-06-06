from drf_spectacular.openapi import OpenApiParameter


AIRPLANE_TYPE_ID = OpenApiParameter(
    name="airplane_type_id",
    type=int,
    description="Filter by id of airplane type"
)
