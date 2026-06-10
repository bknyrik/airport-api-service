from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    UserAdminSerializer,
    UserAdminListRetrieveSerializer
)

User = get_user_model()

USER_ADMIN_LIST_URL = reverse("user:user-list")
USER_REGISTER_URL = reverse("user:register")
USER_MANAGE_URL = reverse("user:manage")


def user_admin_detail_url(pk: int) -> str:
    return reverse("user:user-detail", kwargs={"pk": pk})


def user_sample(**kwargs) -> User:
    defaults = {
        "email": "user@sample.com",
        "password": "userpass12345"
    }
    defaults.update(kwargs)

    return User.objects.create_user(**defaults)


def get_throttle_rate(scope: str) -> int:
    return int(api_settings.DEFAULT_THROTTLE_RATES[scope].split("/")[0])


class UnauthenticatedUserApiTests(APITestCase):

    def test_user_admin_list_authentication_required(self) -> None:
        response = self.client.get(USER_ADMIN_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_admin_retrieve_authentication_required(self) -> None:
        response = self.client.get(user_admin_detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_manage_authentication_required(self) -> None:
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
        self.assertEqual(serializer.data, response.data)
        self.assertTrue(user.check_password(data["password"]))

    def test_user_register_request_is_throttled(self) -> None:
        REGISTER_RATE = get_throttle_rate("register")

        for _ in range(REGISTER_RATE):
            self.client.get(USER_REGISTER_URL)

        response = self.client.get(USER_REGISTER_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )


class AuthenticatedUserApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@airport.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_manage_retrieve(self) -> None:
        response = self.client.get(USER_MANAGE_URL)
        serializer = UserSerializer(self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_user_manage_update(self) -> None:
        data = {
            "email": "upduser@airport.com",
            "first_name": "Update First",
            "last_name": "Update Last",
            "password": "updatepass12345",
        }
        response = self.client.put(USER_MANAGE_URL, data=data)
        serializer = UserSerializer(self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
        self.assertTrue(self.user.check_password(data["password"]))

    def test_user_manage_partial_update(self) -> None:
        data = {
            "email": "upduser@airport.com",
            "first_name": "Update First"
        }
        response = self.client.patch(USER_MANAGE_URL, data=data)
        serializer = UserSerializer(self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_register_user_is_forbidden(self) -> None:
        response = self.client.post(USER_REGISTER_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_admin_list_is_forbidden(self) -> None:
        response = self.client.get(USER_ADMIN_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_admin_retrieve_is_forbidden(self) -> None:
        response = self.client.get(user_admin_detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_manage_request_is_throttled(self) -> None:
        USER_RATE = get_throttle_rate("user")

        for _ in range(USER_RATE):
            self.client.get(USER_MANAGE_URL)

        response = self.client.get(USER_MANAGE_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )

    def test_user_manage_destroy_is_not_allowed(self) -> None:
        response = self.client.delete(USER_MANAGE_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )


class AuthenticatedAdminUserApiTests(APITestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            email="admin@airport.com",
            password="admin123456",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_register_user(self) -> None:
        data = {
            "email": "user@example.com",
            "password": "userpass12345"
        }
        response = self.client.post(USER_REGISTER_URL, data=data)
        user = User.objects.get(email=data["email"])
        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)
        self.assertTrue(user.check_password(data["password"]))

    def test_user_admin_list(self) -> None:
        users = (
            self.admin_user,
            user_sample(),
            user_sample(email="user2@sample.com"),
            user_sample(email="user3@sample.com")
        )

        serializer = UserAdminListRetrieveSerializer(users, many=True)
        response = self.client.get(USER_ADMIN_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_user_admin_list_filter_by_is_staff(self) -> None:
        user = user_sample()
        user2_staff = user_sample(email="user2@sample.com", is_staff=True)
        user3 = user_sample(email="user3@sample.com")
        user4_staff = user_sample(email="user4@sample.com", is_staff=True)

        response = self.client.get(
            USER_ADMIN_LIST_URL,
            query_params={"is_staff": True}
        )

        serializer_user_not_staff = UserAdminListRetrieveSerializer(user)
        serializer_user2_staff = UserAdminListRetrieveSerializer(user2_staff)
        serializer_user3_not_staff = UserAdminListRetrieveSerializer(user3)
        serializer_user4_staff = UserAdminListRetrieveSerializer(user4_staff)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_user2_staff.data, response.data["results"])
        self.assertIn(serializer_user4_staff.data, response.data["results"])
        self.assertNotIn(serializer_user_not_staff, response.data["results"])
        self.assertNotIn(serializer_user3_not_staff, response.data["results"])

    def test_user_admin_list_filter_by_email_characters(self) -> None:
        user = user_sample(email="johndoe@sample.com")
        user2 = user_sample(email="donaldcooper@sample.com")
        user3 = user_sample(email="marksimms@sample.com")

        user_serializer = UserAdminListRetrieveSerializer(user)
        user2_serializer = UserAdminListRetrieveSerializer(user2)
        user3_serializer = UserAdminListRetrieveSerializer(user3)

        response = self.client.get(
            USER_ADMIN_LIST_URL,
            query_params={"email": "do"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(user_serializer.data, response.data["results"])
        self.assertIn(user2_serializer.data, response.data["results"])
        self.assertNotIn(user3_serializer.data, response.data["results"])

    def test_user_admin_list_with_pagination(self) -> None:
        PAGE_SIZE = 2

        user = user_sample()
        user2 = user_sample(email="user2@sample.com")
        user3 = user_sample(email="user3@sample.com")

        response = self.client.get(
            USER_ADMIN_LIST_URL,
            query_params={"page_size": PAGE_SIZE}
        )
        serializer_users = UserAdminListRetrieveSerializer(
            (self.admin_user, user),
            many=True
        )
        serializer_user2 = UserAdminListRetrieveSerializer(user2)
        serializer_user3 = UserAdminListRetrieveSerializer(user3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_users.data, response.data["results"])
        self.assertNotIn(serializer_user2.data, response.data["results"])
        self.assertNotIn(serializer_user3.data, response.data["results"])

    def test_user_admin_create(self) -> None:
        data = {
            "email": "user@example.com",
            "password": "userpass12345",
            "is_staff": True,
            "user_permissions": (1, 2)
        }

        response = self.client.post(USER_ADMIN_LIST_URL, data=data)
        user = User.objects.get(email=data["email"])
        serializer = UserAdminSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_user_admin_retrieve(self) -> None:
        user = user_sample()

        response = self.client.get(user_admin_detail_url(pk=user.id))
        serializer = UserAdminListRetrieveSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_user_admin_update(self) -> None:
        user = user_sample()
        data = {
            "email": "upduser@example.com",
            "first_name": "User",
            "last_name": "Sample",
            "password": "updpass12345",
            "is_superuser": True,
            "user_permissions": (3, 4, 5)
        }
        response = self.client.put(
            user_admin_detail_url(pk=user.pk),
            data=data
        )
        user.refresh_from_db()

        serializer = UserAdminSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
        self.assertTrue(user.check_password(data["password"]))

    def test_user_admin_partial_update(self) -> None:
        user = user_sample(is_staff=True)
        data = {
            "first_name": "User",
            "last_name": "Sample",
            "is_staff": False,
        }

        response = self.client.patch(
            user_admin_detail_url(pk=user.id),
            data=data
        )
        user.refresh_from_db()

        serializer = UserAdminSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_user_admin_destroy(self) -> None:
        user = user_sample()
        response = self.client.delete(user_admin_detail_url(pk=user.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=user.id).exists())

    def test_user_admin_list_request_is_throttled(self) -> None:
        ADMIN_RATE = get_throttle_rate("admin")

        for _ in range(ADMIN_RATE):
            self.client.get(USER_ADMIN_LIST_URL)

        response = self.client.get(USER_ADMIN_LIST_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )
