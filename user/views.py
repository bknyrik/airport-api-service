from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

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


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrAnonymous,)


class ManageUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
