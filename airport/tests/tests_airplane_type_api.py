from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.throttling import default_cache

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer
from user.tests.tests_user_api import get_throttle_rate

User = get_user_model()


AIRPLANE_TYPE_LIST_URL = reverse("airport:airplane-type-list")


def airplane_type_sample(**kwargs) -> AirplaneType:
    defaults = {
        "name": "Airplane Sample",
    }
    defaults.update(kwargs)
    return AirplaneType.objects.create(**defaults)


def get_airplane_type_detail_url(pk: int) -> str:
    return reverse("airport:airplane-type-detail", kwargs={"pk": pk})


class UnauthenticatedAirplaneTypeApiTests(APITestCase):

    def setUp(self) -> None:
        default_cache.clear()
        self.airplane_type_1 = airplane_type_sample()
        self.airplane_type_2 = airplane_type_sample(name="Airplane Sample 2")
        self.airplane_type_3 = airplane_type_sample(name="Airplane Sample 3")

    def test_airplane_type_list(self) -> None:
        airplane_types = (
            self.airplane_type_1,
            self.airplane_type_2,
            self.airplane_type_3,
        )
        response = self.client.get(AIRPLANE_TYPE_LIST_URL)
        serializer = AirplaneTypeSerializer(airplane_types, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_airplane_type_list_with_pagination(self) -> None:
        PAGE_SIZE = 2
        response = self.client.get(
            AIRPLANE_TYPE_LIST_URL,
            query_params={"page_size": PAGE_SIZE}
        )
        serializer_airplane_types = AirplaneTypeSerializer(
            (self.airplane_type_1, self.airplane_type_2),
            many=True
        )
        serializer_airplane_type3 = AirplaneTypeSerializer(
            self.airplane_type_3
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_airplane_types.data, response.data["results"])
        self.assertNotIn(serializer_airplane_type3.data, response.data["results"])

    def test_airplane_type_retrieve(self) -> None:
        URL = get_airplane_type_detail_url(pk=self.airplane_type_1.id)
        response = self.client.get(URL)
        serializer = AirplaneTypeSerializer(self.airplane_type_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_airplane_type_retrieve_request_is_throttled(self) -> None:
        ANON_RATE = get_throttle_rate("anon")
        URL = get_airplane_type_detail_url(pk=self.airplane_type_1.id)

        for _ in range(ANON_RATE):
            self.client.get(URL)

        response = self.client.get(URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )

    def test_airplane_type_create_authentication_required(self) -> None:
        data = {"name": "Test"}
        response = self.client.post(AIRPLANE_TYPE_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_update_authentication_required(self) -> None:
        URL = get_airplane_type_detail_url(pk=self.airplane_type_1.id)
        data = {"name": "Another test"}
        response = self.client.put(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_partial_update_authentication_required(self) -> None:
        URL = get_airplane_type_detail_url(pk=self.airplane_type_1.id)
        data = {"name": "Partial Test"}
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_destroy_authentication_required(self) -> None:
        URL = get_airplane_type_detail_url(pk=self.airplane_type_1.id)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_list_request_is_throttled(self) -> None:
        ANON_RATE = get_throttle_rate("anon")

        for _ in range(ANON_RATE):
            self.client.get(AIRPLANE_TYPE_LIST_URL)

        response = self.client.get(AIRPLANE_TYPE_LIST_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )


class AuthenticatedAirplaneTypeApiTests(APITestCase):

    def setUp(self) -> None:
        default_cache.clear()
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass12345"
        )
        self.client.force_authenticate(user=self.user)

    def test_airplane_type_create_is_forbidden(self) -> None:
        data = {"name": "Test airplane type"}
        response = self.client.post(AIRPLANE_TYPE_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_type_update_is_forbidden(self) -> None:
        data = {"name": "Another test airplane type"}
        URL = get_airplane_type_detail_url(pk=1)
        response = self.client.put(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_type_partial_update_is_forbidden(self) -> None:
        data = {"name": "Partial aitplane type"}
        URL = get_airplane_type_detail_url(pk=1)
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_type_destroy_is_forbidden(self) -> None:
        URL = get_airplane_type_detail_url(pk=1)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_type_list_request_is_throttled(self) -> None:
        USER_RATE = get_throttle_rate("user")

        for _ in range(USER_RATE):
            self.client.get(AIRPLANE_TYPE_LIST_URL)

        response = self.client.get(AIRPLANE_TYPE_LIST_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )

    def test_airplane_type_retrieve_request_is_throttled(self) -> None:
        airplane_type = airplane_type_sample()
        USER_RATE = get_throttle_rate("user")
        URL = get_airplane_type_detail_url(pk=airplane_type.id)

        for _ in range(USER_RATE):
            self.client.get(URL)

        response = self.client.get(URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )


class AdminAirplaneTypeApiTests(APITestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            email="admin@airport.com",
            password="userpass12345",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)
        self.airplane_type = airplane_type_sample()

    def test_airplane_type_create(self) -> None:
        data = {"name": "Test airplane type"}
        response = self.client.post(AIRPLANE_TYPE_LIST_URL, data=data)
        airplane_type = AirplaneType.objects.get(name=data["name"])
        serializer = AirplaneTypeSerializer(airplane_type)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_airplane_type_update(self) -> None:
        data = {"name": "Another test airplane type"}
        URL = get_airplane_type_detail_url(pk=self.airplane_type.id)
        response = self.client.put(URL, data=data)
        serializer = AirplaneTypeSerializer(self.airplane_type)
        self.airplane_type.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_airplane_type_partial_update(self) -> None:
        data = {"name": "Partial airplane type"}
        URL = get_airplane_type_detail_url(pk=self.airplane_type.id)
        response = self.client.patch(URL, data=data)
        serializer = AirplaneTypeSerializer(self.airplane_type)

        self.airplane_type.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_airplane_type_destroy(self) -> None:
        URL = get_airplane_type_detail_url(pk=self.airplane_type.id)
        response = self.client.delete(URL)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AirplaneType.objects.filter(
                name=self.airplane_type.name
            ).exists()
        )

    def test_airplane_type_list_request_is_throttled(self) -> None:
        ADMIN_RATE = get_throttle_rate("admin")

        for _ in range(ADMIN_RATE):
            self.client.get(AIRPLANE_TYPE_LIST_URL)

        response = self.client.get(AIRPLANE_TYPE_LIST_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )

    def test_airplane_type_retrieve_request_is_throttled(self) -> None:
        ADMIN_RATE = get_throttle_rate("admin")
        URL = get_airplane_type_detail_url(pk=self.airplane_type.id)

        for _ in range(ADMIN_RATE):
            self.client.get(URL)

        response = self.client.get(URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )
