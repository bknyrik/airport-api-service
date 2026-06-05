from drf_spectacular.openapi import (
    OpenApiResponse,
    OpenApiTypes
)

from openapi import examples
from user.serializers import UserSerializer


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

USER_IS_NOT_AUTHORIZED = OpenApiResponse(
    description="User is not authorized",
    response={
        "example": {
            "detail": (
                "Authentication credentials were not provided."
            )
        }
    }
)

INVALID_USER_DATA = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Invalid input data",
    examples=[
        examples.EMAIL_IS_INVALID,
        examples.EMAIL_EXISTS,
        examples.EMAIL_IS_BLANK,
        examples.PASSWORD_HAS_INVALID_LENGTH,
        examples.PASSWORD_IS_BLANK
    ]
)

USER_UPDATED_SUCCESSFULLY = OpenApiResponse(
    response=UserSerializer,
    description="User updated successfully",
)

CURRENT_USER_INFORMATION = OpenApiResponse(
    description="Got an information about the current user",
    response=UserSerializer
)

USER_CANT_REGISTER = OpenApiResponse(
    description=(
        "A user, that is not an admin/anonymous, can't register a new user"
    ),
    response={
        "example": {
            "detail": ["You do not have permission to perform this action."]
        },
    },
)

USER_CREATED_SUCCESSFULLY = OpenApiResponse(
    description="User successfully created",
    response=UserSerializer
)

USER_IS_DELETED_SUCCESSFULLY = OpenApiResponse(
    description="User was deleted",
)

USER_NOT_FOUND = OpenApiResponse(
    description="User not found",
    response={"example": {"detail": "No User matches the given query."}}
)

USER_CANT_DELETE = OpenApiResponse(
    description=(
            "A user, that is not an admin, can't delete the user"
    ),
    response={
        "example": {
            "detail": ["You do not have permission to perform this action."]
        }
    }
)
