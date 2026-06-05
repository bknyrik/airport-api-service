from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import (
    OpenApiParameter,
    OpenApiRequest,
    OpenApiExample,
    OpenApiResponse,
    OpenApiTypes
)

from user.serializers import (
    UserSerializer,
    UserAdminSerializer,
    UserAdminListRetrieveSerializer
)
from user.permissions import IsAdminOrAnonymous
from user.pagination import UserSetPagination
from user.filtersets import UserFilterSet


User = get_user_model()


class UserAdminViewSet(ModelViewSet):
    queryset = User.objects.prefetch_related(
        "user_permissions__content_type",
        "groups"
    )
    permission_classes = (IsAdminUser, )
    pagination_class = UserSetPagination
    filterset_class = UserFilterSet

    def get_serializer_class(self) -> type[UserSerializer]:
        if self.action in ("list", "retrieve"):
            return UserAdminListRetrieveSerializer

        return UserAdminSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                description="Filter by characters that are in email.",
            ),
            OpenApiParameter(
                name="is_staff",
                type=bool,
                description="Filter by status if user is an admin."
            )
        ],
        description=(
            "Returns list with users. This list also can be filtered by "
            "email pattern, is_staff status and paginated by "
            "page and page_size query parameters."
        ),
        summary="Get all users"
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes user credentials, including permissions, "
            "certain groups and an admin status, and returns "
            "a new user"
        ),
        summary="Create a user"
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Returns detailed information about user,"
            " including permissions, groups and status."
        ),
        summary="Get user by id"
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes all user credentials, including permissions, "
            "groups and an admin status, and returns updated information "
            "about the user by id."
        ),
        summary="Completely update the user by id"
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes specified user credentials and "
            "returns updated information about the user by id."
        ),
        summary="Partially update the user by id"
    )
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Deletes the user by id and returns nothing.",
        summary="Delete the user by id"
    )
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        return super().destroy(request, *args, **kwargs)


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrAnonymous,)
    throttle_scope = "register"

    @extend_schema(
        description=(
            "Takes user credentials and returns information "
            "about new created user."
        ),
        summary="Register a new user",
        request=OpenApiRequest(
            request=UserSerializer,
            examples=[
                OpenApiExample(
                    name="Register a user with all fields",
                    value={
                        "email": "user@example.com",
                        "first_name": "User First",
                        "last_name": "User Last",
                        "password": "userpass12345"
                    },
                ),
                OpenApiExample(
                    name="Register a user with email and password fields",
                    description=(
                        "Fields first_name and last_name are optional."
                    ),
                    value={
                        "email": "user@example.com",
                        "password": "userpass12345"
                    },
                )
            ]
        ),
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="User successfully created",
                response=UserSerializer,
                examples=[
                    OpenApiExample(
                        name="User created with all provided fields",
                        value={
                            "id": 1,
                            "email": "user@example.com",
                            "first_name": "User First",
                            "last_name": "User Last",
                            "is_staff": False
                        },
                    ),
                    OpenApiExample(
                        name="User created with provided field email",
                        value={
                            "id": 1,
                            "email": "user@example.com",
                            "first_name": "",
                            "last_name": "",
                            "is_staff": False
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid input data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Email is invalid",
                        value={"email": ["Enter a valid email address."]}
                    ),
                    OpenApiExample(
                        name="Email already exists",
                        value={
                            "email": [
                                "user with this Email address already exists."
                            ],
                        },
                    ),
                    OpenApiExample(
                        name="Password has invalid length",
                        value={
                            "password": [
                                "Ensure this field has at least 8 characters."
                            ]
                        },
                    ),
                    OpenApiExample(
                        name="Email is blank",
                        value={"email": ["This field may not be blank."],}
                    ),
                    OpenApiExample(
                        name="Password is blank",
                        value={"password": ["This field may not be blank."],}
                    ),
                ]
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response={
                    "example": {
                        "detail": [
                            (
                                "You do not have permission "
                                "to perform this action."
                            )
                        ]
                    },
                },
                description=(
                    "A user, that is not an admin/anonymous, can't register"
                    " a new user"
                ),
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                description="User exhausted the limit of requests",
                response={
                    "example": {
                        "detail": (
                            "Request was throttled. "
                            "Expected available in 86399 seconds."
                        )
                    }
                }
            )
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class ManageUserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user

    @extend_schema(
        description="Returns information about the current authorized user.",
        summary="Get the current authorized user",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Got an information about the current user",
                response={
                    "example": {
                        "email": "user@example.com",
                        "first_name": "User First",
                        "last_name": "User Last",
                        "is_staff": False
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authorized",
                response={
                    "example": {
                      "detail": (
                          "Authentication credentials were not provided."
                      )
                    }
                }
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                description="User exhausted the limit of requests",
                response={
                    "example": {
                        "detail": (
                            "Request was throttled. "
                            "Expected available in 86399 seconds."
                        )
                    }
                }
            )
        }
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes all user credentials and returns "
            "updated information about the current authorized user."
        ),
        summary="Completely update the current user",
        request=OpenApiRequest(
            request=UserSerializer,
            examples=[
                OpenApiExample(
                    name="Update user with all fields",
                    value={
                        "email": "upd_user@example.com",
                        "first_name": "Update First",
                        "last_name": "Update Last",
                        "password": "updpass12345"
                    }
                ),
                OpenApiExample(
                    name="Update user with fields email and password",
                    description=(
                        "Fields first_name and last_name are optional."
                    ),
                    value={
                        "email": "upd_user@example.com",
                        "password": "updpass12345"
                    }
                ),
            ]
        ),
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="User is updated successfully",
                examples=[
                    OpenApiExample(
                        name="User is updated with all fields",
                        value={
                            "id": 1,
                            "email": "upd_user@example.com",
                            "first_name": "Update First",
                            "last_name": "Update Last",
                            "password": "updpass12345"
                        }
                    ),
                    OpenApiExample(
                        name="User is updated with fields email and password",
                        description="Fields first_name and last_name may be blank.",
                        value={
                            "id": 1,
                            "email": "upd_user@example.com",
                            "first_name": "",
                            "last_name": "",
                            "password": "updpass12345"
                        }
                    )
                ]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Invalid input data",
                examples=[
                    OpenApiExample(
                        name="Email is invalid",
                        value={"email": ["Enter a valid email address."]}
                    ),
                    OpenApiExample(
                        name="Email is blank",
                        value={"email": ["This field may not be blank."]}
                    ),
                    OpenApiExample(
                        name="Password has invalid length",
                        value={
                            "password": [
                                "Ensure this field has at least 8 characters."
                            ]
                        }
                    ),
                    OpenApiExample(
                        name="Password is blank",
                        value={"password": ["This field may not be blank."]}
                    )
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authorized",
                response={
                    "example": {
                        "detail": (
                            "Authentication credentials were not provided."
                        )
                    }
                }
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                description="User exhausted the limit of requests",
                response={
                    "example": {
                        "detail": (
                            "Request was throttled. "
                            "Expected available in 86399 seconds."
                        )
                    }
                }
            )
        }
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes specified user credentials and returns "
            "updated information about the current authorized user."
        ),
        summary="Partially update the current user",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="User updated successfully",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Invalid input data",
                examples=[
                    OpenApiExample(
                        name="Email is invalid",
                        value={"email": ["Enter a valid email address."]}
                    ),
                    OpenApiExample(
                        name="Email already exists",
                        value={
                            "email": [
                                "user with this Email address already exists."
                            ],
                        },
                    ),
                    OpenApiExample(
                        name="Email is blank",
                        value={"email": ["This field may not be blank."]}
                    ),
                    OpenApiExample(
                        name="Password has invalid length",
                        value={
                            "password": [
                                "Ensure this field has at least 8 characters."
                            ]
                        }
                    ),
                    OpenApiExample(
                        name="Password is blank",
                        value={"password": ["This field may not be blank."]}
                    )
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authorized",
                response={
                    "example": {
                        "detail": (
                            "Authentication credentials were not provided."
                        )
                    }
                }
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                description="User exhausted the limit of requests",
                response={
                    "example": {
                        "detail": (
                            "Request was throttled. "
                            "Expected available in 86399 seconds."
                        )
                    }
                }
            )
        }
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)
