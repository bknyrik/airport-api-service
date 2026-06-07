from rest_framework import status
from drf_spectacular.openapi import (
    OpenApiResponse,
    OpenApiTypes
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer
)

from openapi.user import examples
from user.serializers import (
    UserSerializer,
    UserAdminSerializer,
    UserAdminListRetrieveSerializer
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

GOT_USER_INFO = OpenApiResponse(
    response=UserSerializer,
    description="Got user information"
)

USER_IS_CREATED = OpenApiResponse(
    description="User is created",
    response=UserSerializer
)

USER_IS_DELETED = OpenApiResponse(
    description="User is deleted",
)

USER_NOT_FOUND = OpenApiResponse(
    description="User not found",
    response={"example": {"detail": "No User matches the given query."}}
)

USER_IS_NOT_ADMIN = OpenApiResponse(
    description="User is not an admin to perform this action",
    response={
        "example": {
            "detail": "You do not have permission to perform this action."
        }
    }
)

USER_IS_NOT_ADMIN_OR_ANON = OpenApiResponse(
    description="A user is not an admin/anonymous to perform this action",
    response=USER_IS_NOT_ADMIN.response,
)

USER_IS_UNAUTHORIZED = OpenApiResponse(
    description="User is not authorized",
    response={
        "example": {"detail": "Authentication credentials were not provided."}
    }
)

USER_REACHED_LIMIT_REQUESTS = OpenApiResponse(
    description="User reached the limit of requests",
    response={
        "example": {
            "detail": (
                "Request was throttled. Expected available in 86399 seconds."
            )
        }
    }
)

USER_REGISTER_RESPONSES = {
    status.HTTP_201_CREATED: USER_IS_CREATED,
    status.HTTP_400_BAD_REQUEST: INVALID_USER_DATA,
    status.HTTP_403_FORBIDDEN: USER_IS_NOT_ADMIN_OR_ANON,
    status.HTTP_429_TOO_MANY_REQUESTS: USER_REACHED_LIMIT_REQUESTS
}

USER_GET_RESPONSES = {
    status.HTTP_200_OK: GOT_USER_INFO,
}

USER_PUT_RESPONSES = {
    status.HTTP_200_OK: GOT_USER_INFO,
    status.HTTP_400_BAD_REQUEST: INVALID_USER_DATA,
}

USER_PATCH_RESPONSES = USER_PUT_RESPONSES

USER_ADMIN_IS_CREATED = OpenApiResponse(
    response=UserAdminSerializer,
    description="User is created",
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

GOT_USER_ADMIN_INFO = OpenApiResponse(
    response=UserAdminListRetrieveSerializer,
    description="Got the extended information about the user by id"
)

GOT_USERS_ADMIN_INFO = OpenApiResponse(
    description="Got an extended information about the users",
    response=UserAdminListRetrieveSerializer
)

PAGE_NOT_FOUND = OpenApiResponse(
    description="User specified the non-existent page",
    response={"example": {"detail": "Invalid page."}}
)

USER_LIST_RESPONSES = {
    status.HTTP_200_OK: GOT_USERS_ADMIN_INFO,
    status.HTTP_404_NOT_FOUND: PAGE_NOT_FOUND,
}

USER_CREATE_RESPONSES = {
    status.HTTP_201_CREATED: USER_ADMIN_IS_CREATED,
    status.HTTP_400_BAD_REQUEST: USER_ADMIN_INVALID_DATA,
}

USER_ADMIN_RETRIEVE_RESPONSES = {
    status.HTTP_200_OK: GOT_USER_ADMIN_INFO,
    status.HTTP_404_NOT_FOUND: USER_NOT_FOUND,
}

USER_ADMIN_UPDATE_RESPONSES = {
    status.HTTP_200_OK: GOT_USER_ADMIN_INFO,
    status.HTTP_400_BAD_REQUEST: USER_ADMIN_INVALID_DATA,
    status.HTTP_404_NOT_FOUND: USER_NOT_FOUND,
}

USER_ADMIN_PARTIAL_UPDATE_RESPONSES = USER_ADMIN_UPDATE_RESPONSES

USER_ADMIN_DESTROY_RESPONSES = {
    status.HTTP_204_NO_CONTENT: USER_IS_DELETED,
    status.HTTP_404_NOT_FOUND: USER_NOT_FOUND,
}

ACCOUNT_NOT_FOUND = OpenApiResponse(
    description="Account with provided credentials not found",
    response={
        "example": {
            "detail": "No active account found with the given credentials"
        }
    }
)

GOT_ACCESS_AND_REFRESH_TOKENS = OpenApiResponse(
    description="Got access and refresh tokens",
    response=TokenObtainPairSerializer
)

TOKEN_IS_INVALID = OpenApiResponse(
    description="Provided refresh token is not valid",
    response={
        "example": {
            "detail": "Token is invalid",
            "code": "token_not_valid"
        }
    }
)

GOT_ACCESS_TOKEN = OpenApiResponse(
    description="Got a new access token",
    response=TokenRefreshSerializer
)

TOKEN_IS_VALID = OpenApiResponse(
    description="Provided token is valid",
    response={"example": {}}
)

TOKEN_IS_INVALID_OR_EXPIRED = OpenApiResponse(
    description="Token is invalid",
    response=TokenVerifySerializer,
    examples=[examples.TOKEN_IS_INVALID, examples.TOKEN_IS_EXPIRED]
)

TOKEN_OBTAIN_POST_RESPONSES = {
    status.HTTP_200_OK: GOT_ACCESS_AND_REFRESH_TOKENS,
    status.HTTP_401_UNAUTHORIZED: ACCOUNT_NOT_FOUND,
}

TOKEN_REFRESH_POST_RESPONSES = {
    status.HTTP_200_OK: GOT_ACCESS_TOKEN,
    status.HTTP_401_UNAUTHORIZED: TOKEN_IS_INVALID,
}

TOKEN_VERIFY_POST_RESPONSES = {
    status.HTTP_200_OK: TOKEN_IS_VALID,
    status.HTTP_401_UNAUTHORIZED: TOKEN_IS_INVALID_OR_EXPIRED,
}
