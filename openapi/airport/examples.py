from drf_spectacular.openapi import OpenApiExample


AIRPLANE_TYPE_NAME_EXISTS = OpenApiExample(
    name="Airplane type exists",
    value={"name": ["airplane type with this name already exists."]}
)
