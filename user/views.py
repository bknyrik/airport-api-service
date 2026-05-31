from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from user.serializers import (
    UserSerializer,
    UserAdminSerializer,
    UserAdminListRetrieveSerializer
)


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.prefetch_related(
        "user_permissions__content_type",
        "groups"
    )

    def get_serializer_class(self) -> type[UserSerializer]:
        if self.action in ("list", "retrieve"):
            return UserAdminListRetrieveSerializer

        return UserAdminSerializer


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user
