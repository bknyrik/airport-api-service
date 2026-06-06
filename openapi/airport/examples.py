from drf_spectacular.openapi import OpenApiExample


AIRPLANE_TYPE_NAME_EXISTS = OpenApiExample(
    name="Name already exists",
    value={"name": ["airplane type with this name already exists."]}
)

NAME_IS_BLANK = OpenApiExample(
    name="Name is blank",
    value={"name": ["This field may not be blank."]}
)
