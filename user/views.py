from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView as JWTTokenObtainPairView,
    TokenRefreshView as JWTTokenRefreshView,
    TokenVerifyView as JWTTokenVerifyView
)

from user.serializers import (
    UserSerializer,
    UserAdminSerializer,
    UserAdminListRetrieveSerializer
)
from user.permissions import IsAdminOrAnonymous
from user.pagination import UserSetPagination
from user.filtersets import UserFilterSet
from openapi.user import parameters, responses

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
            parameters.FILTER_BY_EMAIL_PATTERN,
            parameters.FILTER_BY_IS_STAFF
        ],
        description=(
            "Returns list with users. This list also can be filtered by "
            "email pattern, is_staff status and paginated by "
            "page and page_size query parameters."
        ),
        summary="Get all users",
        responses={
            status.HTTP_200_OK: responses.GOT_USERS_ADMIN_INFO,
            status.HTTP_401_UNAUTHORIZED: responses.USER_IS_NOT_AUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.USER_IS_NOT_ADMIN,
            status.HTTP_404_NOT_FOUND: responses.PAGE_NOT_FOUND,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED,
        }
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes user credentials, including permissions, "
            "certain groups and an admin status, and returns "
            "a new user"
        ),
        summary="Create a user",
        responses={
            status.HTTP_201_CREATED: responses.USER_IS_CREATED,
            status.HTTP_401_UNAUTHORIZED: responses.USER_IS_NOT_AUTHORIZED,
            status.HTTP_400_BAD_REQUEST: responses.USER_ADMIN_INVALID_DATA,
            status.HTTP_403_FORBIDDEN: responses.USER_IS_NOT_ADMIN,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED
        }
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Returns detailed information about user,"
            " including permissions, groups and status."
        ),
        summary="Get user by id",
        responses={
            status.HTTP_200_OK: responses.GOT_USER_ADMIN_INFO,
            status.HTTP_401_UNAUTHORIZED: responses.USER_IS_NOT_AUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.USER_IS_NOT_ADMIN,
            status.HTTP_404_NOT_FOUND: responses.USER_NOT_FOUND,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED
        }
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes all user credentials, including permissions, "
            "groups and an admin status, and returns updated information "
            "about the user by id."
        ),
        summary="Completely update the user by id",
        responses={
            status.HTTP_200_OK: responses.USER_ADMIN_IS_UPDATED_SUCCESSFULLY,
            status.HTTP_400_BAD_REQUEST: responses.USER_ADMIN_INVALID_DATA,
            status.HTTP_401_UNAUTHORIZED: responses.USER_IS_NOT_AUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.USER_IS_NOT_ADMIN,
            status.HTTP_404_NOT_FOUND: responses.USER_NOT_FOUND,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED
        }
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes specified user credentials and "
            "returns updated information about the user by id."
        ),
        summary="Partially update the user by id",
        responses={
            status.HTTP_200_OK: responses.USER_ADMIN_IS_UPDATED_SUCCESSFULLY,
            status.HTTP_400_BAD_REQUEST: responses.USER_ADMIN_INVALID_DATA,
            status.HTTP_401_UNAUTHORIZED: responses.USER_IS_NOT_AUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.USER_IS_NOT_ADMIN,
            status.HTTP_404_NOT_FOUND: responses.USER_NOT_FOUND,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED
        }
    )
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Deletes the user by id and returns nothing.",
        summary="Delete the user by id",
        responses={
            status.HTTP_204_NO_CONTENT: responses.USER_IS_DELETED,
            status.HTTP_401_UNAUTHORIZED: responses.USER_IS_NOT_AUTHORIZED,
            status.HTTP_404_NOT_FOUND: responses.USER_NOT_FOUND,
            status.HTTP_403_FORBIDDEN: responses.USER_IS_NOT_ADMIN,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED
        }
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
        responses=responses.USER_REGISTER_RESPONSES,
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
        responses=responses.USER_GET_RESPONSES
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes all user credentials and returns "
            "updated information about the current authorized user."
        ),
        summary="Completely update the current user",
        responses=responses.USER_PUT_RESPONSES
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes specified user credentials and returns "
            "updated information about the current authorized user."
        ),
        summary="Partially update the current user",
        responses=responses.USER_PATCH_RESPONSES
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)


class TokenObtainPairView(JWTTokenObtainPairView):

    @extend_schema(
        summary="Get access and refresh tokens",
        responses={
            status.HTTP_200_OK: responses.GOT_ACCESS_AND_REFRESH_TOKENS,
            status.HTTP_401_UNAUTHORIZED: responses.ACCOUNT_NOT_FOUND,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED,
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenRefreshView(JWTTokenRefreshView):

    @extend_schema(
        summary="Refresh an access token",
        responses={
            status.HTTP_200_OK: responses.GOT_ACCESS_TOKEN,
            status.HTTP_401_UNAUTHORIZED: responses.TOKEN_IS_INVALID,
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED,
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenVerifyView(JWTTokenVerifyView):

    @extend_schema(
        summary="Verify the token",
        responses={
            status.HTTP_200_OK: responses.TOKEN_IS_VALID,
            status.HTTP_401_UNAUTHORIZED: (
                responses.TOKEN_IS_INVALID_OR_EXPIRED
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: responses.REQUEST_IS_THROTTLED
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
