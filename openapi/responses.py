from drf_spectacular.openapi import (
    OpenApiResponse,
    OpenApiTypes
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)

from openapi import examples
from user.serializers import (
    UserSerializer,
    UserAdminSerializer,
    UserAdminListRetrieveSerializer
)


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

USER_CANT_UPDATE = OpenApiResponse(
    description="A user, that is not an admin, can't update the user",
    response={
        "example": {
            "detail": ["You do not have permission to perform this action."]
        }
    }
)

USER_ADMIN_IS_UPDATED_SUCCESSFULLY = OpenApiResponse(
    response=UserAdminSerializer,
    description="User is updated successfully",
)

USER_ADMIN_INVALID_DATA = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Invalid input data",
    examples=[
        examples.EMAIL_IS_INVALID,
        examples.EMAIL_EXISTS,
        examples.EMAIL_IS_BLANK,
        examples.PASSWORD_HAS_INVALID_LENGTH,
        examples.PASSWORD_IS_BLANK,
        examples.USER_PERMISSIONS_INVALID_PK,
        examples.GROUPS_INVALID_PK
    ]
)

USER_BY_ID_INFORMATION = OpenApiResponse(
    response=UserAdminSerializer,
    description="Got the extended information about the user by id"
)

USER_CANT_RETRIEVE_USER_INFO = OpenApiResponse(
    description=(
        "User, that is not an admin, "
        "can't retrieve the information about a user"
    ),
    response={
        "example": {
            "detail": ["You do not have permission to perform this action."]
        }
    }
)

USER_CANT_CREATE = OpenApiResponse(
    description="User, that is not an admin, can't create the user",
    response={
        "example": {
            "detail": ["You do not have permission to perform this action"]
        }
    }
)

GOT_USERS_INFORMATION = OpenApiResponse(
    description="Got an extended information about the users",
    response=UserAdminListRetrieveSerializer
)

USER_CANT_GET_USER_LIST = OpenApiResponse(
    description="User, that is not an admin, can get list with users",
    response={
        "example": {
            "detail": ["You do not have permission to perform this action"]
        }
    }
)

PAGE_NOT_FOUND = OpenApiResponse(
    description="User specified the non-existent page",
    response={"example": {"detail": "Invalid page."}}
)

ACCOUNT_NOT_FOUND = OpenApiResponse(
    description="Account with provided credentials not found",
    response={"detail": "No active account found with the given credentials"}
)

GOT_ACCESS_AND_REFRESH_TOKENS = OpenApiResponse(
    description="Got access and refresh tokens",
    response=TokenObtainPairSerializer
)
