from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer


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

    def test_airplane_type_list(self) -> None:
        airplane_type = airplane_type_sample()
        airplane_type2 = airplane_type_sample(name="Airplane Sample 2")

        response = self.client.get(AIRPLANE_TYPE_LIST_URL)
        serializer = AirplaneTypeSerializer(
            (airplane_type, airplane_type2),
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_airplane_type_list_with_pagination(self) -> None:
        PAGE_SIZE = 2
        airplane_type = airplane_type_sample()
        airplane_type2 = airplane_type_sample(name="Airplane Sample 2")
        airplane_type3 = airplane_type_sample(name="Airplane Sample 3")
        response = self.client.get(
            AIRPLANE_TYPE_LIST_URL,
            query_params={"page_size": PAGE_SIZE}
        )
        serializer_airplane_types = AirplaneTypeSerializer(
            (airplane_type, airplane_type2),
            many=True
        )
        serializer_airplane_type3 = AirplaneTypeSerializer(airplane_type3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_airplane_types.data, response.data["results"])
        self.assertNotIn(serializer_airplane_type3.data, response.data["results"])

    def test_airplane_type_retrieve(self) -> None:
        airplane_type = airplane_type_sample()
        response = self.client.get(
            get_airplane_type_detail_url(airplane_type.id)
        )
        serializer = AirplaneTypeSerializer(airplane_type)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_airplane_type_create_authentication_required(self) -> None:
        data = {"name": "Test"}
        response = self.client.post(AIRPLANE_TYPE_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_update_authentication_required(self) -> None:
        data = {"name": "Another test"}
        response = self.client.put(
            get_airplane_type_detail_url(pk=999),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_partial_update_authentication_required(self) -> None:
        data = {"name": "Partial Test"}
        response = self.client.patch(
            get_airplane_type_detail_url(pk=999),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_destroy_authentication_required(self) -> None:
        response = self.client.delete(get_airplane_type_detail_url(pk=999))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass12345"
        )
        self.client.force_authenticate(user=self.user)
