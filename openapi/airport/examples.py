from drf_spectacular.openapi import OpenApiExample


AIRPLANE_TYPE_NAME_EXISTS = OpenApiExample(
    name="Name already exists",
    value={"name": ["airplane type with this name already exists."]}
)

NAME_IS_BLANK = OpenApiExample(
    name="Name is blank",
    value={"name": ["This field may not be blank."]}
)

NAME_HAS_INVALID_LENGTH = OpenApiExample(
    name="Name has invalid length",
    value={"name": ["Ensure this field has no more than 64 characters."]}
)

AIRPLANE_TYPE_ID_INVALID_CHOICE = OpenApiExample(
    name="Airplane type id is invalid",
    value={
        "airplane_type_id": [
            (
                "Select a valid choice. "
                "That choice is not one of the available choices."
            )
        ]
    }
)
