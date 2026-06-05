from drf_spectacular.openapi import OpenApiParameter


FILTER_BY_EMAIL_PATTERN = OpenApiParameter(
    name="email",
    description="Filter by characters, that are in email.",
)
