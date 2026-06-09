from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from user.serializers import UserSerializer

User = get_user_model()

USER_ADMIN_LIST_URL = reverse("user:user-list")


class UnauthenticatedUserApiTests(APITestCase):

    def test_user_admin_list_login_required(self) -> None:
        url = reverse("user:user-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_admin_retrieve_login_required(self) -> None:
        url = reverse("user:user-detail", kwargs={"pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_manage_login_required(self) -> None:
        url = reverse("user:manage")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_allowed_to_register(self) -> None:
        data = {
            "email": "user@airport.com",
            "password": "userpass12345"
        }

        url = reverse("user:register")
        response = self.client.post(url, data=data)

        user = User.objects.get(email=data["email"])

        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data["email"], data["email"])
        self.assertTrue(user.check_password(data["password"]))
