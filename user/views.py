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
        parameters=parameters.USER_LIST_PARAMETERS,
        description=(
            "Returns list with users. This list also can be filtered by "
            "email pattern, is_staff status and paginated by "
            "page and page_size query parameters."
        ),
        summary="Get all users",
        responses=responses.USER_LIST_RESPONSES
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
        responses=responses.USER_CREATE_RESPONSES
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Returns detailed information about user,"
            " including permissions, groups and status."
        ),
        summary="Get user by id",
        responses=responses.USER_ADMIN_RETRIEVE_RESPONSES
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
        responses=responses.USER_ADMIN_UPDATE_RESPONSES
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description=(
            "Takes specified user credentials and "
            "returns updated information about the user by id."
        ),
        summary="Partially update the user by id",
        responses=responses.USER_ADMIN_PARTIAL_UPDATE_RESPONSES
    )
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Deletes the user by id and returns nothing.",
        summary="Delete the user by id",
        responses=responses.USER_ADMIN_DESTROY_RESPONSES
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
        responses=responses.TOKEN_OBTAIN_POST_RESPONSES
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenRefreshView(JWTTokenRefreshView):

    @extend_schema(
        summary="Refresh an access token",
        responses=responses.TOKEN_REFRESH_POST_RESPONSES
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenVerifyView(JWTTokenVerifyView):

    @extend_schema(
        summary="Verify the token",
        responses=responses.TOKEN_VERIFY_POST_RESPONSES
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
