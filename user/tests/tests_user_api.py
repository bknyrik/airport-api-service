from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.settings import api_settings

from user.serializers import UserSerializer

User = get_user_model()

USER_ADMIN_LIST_URL = reverse("user:user-list")
USER_REGISTER_URL = reverse("user:register")
USER_MANAGE_URL = reverse("user:manage")


def user_admin_detail_url(pk: int) -> str:
    return reverse("user:user-detail", kwargs={"pk": pk})


class UnauthenticatedUserApiTests(APITestCase):

    def test_user_admin_list_login_required(self) -> None:
        response = self.client.get(USER_ADMIN_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_admin_retrieve_login_required(self) -> None:
        response = self.client.get(user_admin_detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_manage_login_required(self) -> None:
        response = self.client.get(USER_MANAGE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_allowed_to_register(self) -> None:
        data = {
            "email": "user@airport.com",
            "password": "userpass12345"
        }
        response = self.client.post(USER_REGISTER_URL, data=data)
        user = User.objects.get(email=data["email"])
        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data["email"], data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_request_to_register_url_was_throttled(self) -> None:
        ANON_RATES = int(
            api_settings.DEFAULT_THROTTLE_RATES["anon"].split("/")[0]
        )

        for _ in range(ANON_RATES):
            self.client.get(USER_REGISTER_URL)

        response = self.client.get(USER_REGISTER_URL)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class AuthenticatedUserApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@airport.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)

    def test_manage_user_retrieve(self) -> None:
        response = self.client.get(USER_MANAGE_URL)
        serializer = UserSerializer(self.user)

        self.assertEqual(serializer.data, response.data)
