from drf_spectacular.openapi import OpenApiExample


EMAIL_IS_INVALID = OpenApiExample(
    name="Email is invalid",
    value={"email": ["Enter a valid email address."]}
)

EMAIL_EXISTS = OpenApiExample(
    name="Email already exists",
    value={"email": ["user with this Email address already exists."]}
)
