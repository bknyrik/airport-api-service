from django.contrib.auth import get_user_model
from rest_framework import generics

from user.serializers import UserSerializer


User = get_user_model()


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user
