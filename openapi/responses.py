from drf_spectacular.openapi import OpenApiResponse


REQUEST_IS_THROTTLED = OpenApiResponse(
    description="The user reached the limit of requests",
    response={
        "example": {
            "detail": (
                "Request was throttled. "
                "Expected available in 86399 seconds."
            )
        }
    }
)
