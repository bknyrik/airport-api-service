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

AIRPLANE_TYPE_INVALID_PK = OpenApiExample(
    name="Airplane type pk is invalid",
    value={"airplane_type": ["Invalid pk \"9999\" - object does not exist."]}
)

FACILITIES_INVALID_CHOICE = OpenApiExample(
    name="Facilities id is invalid",
    value={
      "facilities": [
          "Select a valid choice. 9999999 is not "
          "one of the available choices."
      ]
    }
)

FACILITIES_INVALID_PK = OpenApiExample(
    name="Facilities pk is invalid",
    value={"facilities": ["Invalid pk \"0\" - object does not exist."]}
)

ROWS_LESS_THAN_ONE = OpenApiExample(
    name="Rows are less than 1",
    value={"rows": ["Ensure this value is greater than or equal to 1."]}
)

SEATS_IN_ROW_LESS_THAN_ONE = OpenApiExample(
    name="Seats in row are less than 1",
    value={
        "seats_in_row": ["Ensure this value is greater than or equal to 1."]
    }
)
