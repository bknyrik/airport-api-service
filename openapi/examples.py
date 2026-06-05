from drf_spectacular.openapi import OpenApiExample


EMAIL_IS_INVALID = OpenApiExample(
    name="Email is invalid",
    value={"email": ["Enter a valid email address."]}
)

EMAIL_EXISTS = OpenApiExample(
    name="Email already exists",
    value={"email": ["user with this Email address already exists."]}
)

EMAIL_IS_BLANK = OpenApiExample(
    name="Email is blank",
    value={"email": ["This field may not be blank."]}
)

PASSWORD_HAS_INVALID_LENGTH = OpenApiExample(
    name="Password has invalid length",
    value={
        "password": [
            "Ensure this field has at least 8 characters."
        ]
    }
)

PASSWORD_IS_BLANK = OpenApiExample(
    name="Password is blank",
    value={"password": ["This field may not be blank."]}
)

USER_PERMISSIONS_INVALID_PK = OpenApiExample(
    name="Invalid pk for user_permissions",
    value={
        "user_permissions": [
            "Invalid pk \"9999\" - object does not exist."
        ]
    }
)

GROUPS_INVALID_PK = OpenApiExample(
    name="Invalid pk for groups",
    value={
        "groups": [
            "Invalid pk \"9999\" - object does not exist."
        ]
    }
)

TOKEN_IS_INVALID = OpenApiExample(
    name="Provided refresh token is not valid",
    value={
        "example": {
            "detail": "Token is invalid",
            "code": "token_not_valid"
        }
    }
)

TOKEN_IS_EXPIRED = OpenApiExample(
    name="Provided access token is expired",
    value={
        "example": {
            "detail": "Token is expired",
            "code": "token_not_valid"
        }
    }
)
