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

IMAGE_WAS_NOT_A_FILE = OpenApiExample(
    name="Provided data was not a file.",
    value={
        "image": [
            (
                "The submitted data was not a file. "
                "Check the encoding type on the form."
            )
        ]
    }
)

IMAGE_IS_NOT_VALID = OpenApiExample(
    name="File was not an image or corrupted",
    value={
        "image": [
            (
                "Upload a valid image. The file you uploaded was either "
                "not an image or a corrupted image."
            )
        ]
    }
)

AIRPORT_EXISTS = OpenApiExample(
    name="Airport with this data exists",
    value={
        "non_field_errors": [
            "Airport with this name, country and city exists."
        ]
    }
)

AIRPORT_IATA_CODE_IS_INVALID = OpenApiExample(
    name="IATA code is invalid",
    value={
        "iata_code": [
            "IATA code must be a three-letter identifier in upper case"
        ]
    }
)

COUNTRY_IS_BLANK = OpenApiExample(
    name="Country is blank",
    value={"country": ["This field may not be blank."]}
)

CITY_IS_BLANK = OpenApiExample(
    name="City is blank",
    value={"city": ["This field may not be blank."]}
)

FIRST_NAME_IS_BLANK = OpenApiExample(
    name="First name is blank",
    value={"first_name": ["This field may not be blank."]}
)

FIRST_NAME_HAS_INVALID_LENGTH = OpenApiExample(
    name="First name has invalid length",
    value={
        "first_name": ["Ensure this field has no more than 64 characters."]
    }
)

LAST_NAME_IS_BLANK = OpenApiExample(
    name="Last name is blank",
    value={"last_name": ["This field may not be blank."]}
)

LAST_NAME_HAS_INVALID_LENGTH = OpenApiExample(
    name="Last name has invalid length",
    value={
        "last_name": ["Ensure this field has no more than 64 characters."]
    }
)

ROLE_INVALID_CHOICE = OpenApiExample(
    name="Role has invalid choice",
    value={"role": ["\"BB\" is not a valid choice."]}
)

FACILITY_NAME_EXISTS = OpenApiExample(
    name="Facility with this name exists",
    value={"name": ["facility with this name already exists."]}
)

AIRPLANE_ID_INVALID_CHOICE = OpenApiExample(
    name="Airplane id is invalid choice",
    value={
        "airplane_id": [
            "Select a valid choice. "
            "That choice is not one of the available choices."
        ]
    }
)

ROUTE_ID_INVALID_CHOICE = OpenApiExample(
    name="Route id is invalid choice",
    value={
        "route_id": [
            "Select a valid choice. "
            "That choice is not one of the available choices."
        ]
    }
)

CREWMEMBERS_INVALID_CHOICE = OpenApiExample(
    name="Crewmember id is invalid choice",
    value={
        "crewmembers": [
            "Select a valid choice. "
            "99999 is not one of the available choices."
        ]
    }
)

ROUTE_INVALID_PK = OpenApiExample(
    name="Route pk is invalid",
    value={"route": ["Invalid pk \"999\" - object does not exist."]}
)

AIRPLANE_INVALID_PK = OpenApiExample(
    name="Airplane pk is invalid",
    value={"airplane": ["Invalid pk \"999\" - object does not exist."]}
)

CREWMEMBERS_INVALID_PK = OpenApiExample(
    name="Crewmembers pk is invalid",
    value={"crewmembers": ["Invalid pk \"999\" - object does not exist."]}
)

DEPARTURE_TIME_GREATER_THAN_ARRIVAL_TIME = OpenApiExample(
    name="Departure time greater than arrival time",
    value={
        "departure_time": [
            "Departure time must be less than or equal arrival time"
        ]
    }
)

CREWMEMBERS_IS_EMPTY = OpenApiExample(
    name="Crewmembers is empty.",
    value={"crewmembers": ["This list may not be empty."]}
)
