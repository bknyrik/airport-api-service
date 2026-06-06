from drf_spectacular.openapi import OpenApiParameter


FILTER_BY_EMAIL_PATTERN = OpenApiParameter(
    name="email",
    description="Filter by characters, that are in email.",
)

FILTER_BY_IS_STAFF = OpenApiParameter(
    name="is_staff",
    type=bool,
    description="Filter by status if user is an admin."
)

USER_LIST_PARAMETERS = [
    FILTER_BY_EMAIL_PATTERN,
    FILTER_BY_IS_STAFF
]
