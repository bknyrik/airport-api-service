import os
import tempfile

from PIL import Image
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import Airplane
from airport.serializers import AirplaneListRetrieveSerializer
from airport.tests.tests_airplane_type_api import airplane_type_sample
from airport.tests.tests_facility_api import facility_sample


User = get_user_model()


AIRPLANE_LIST_URL = reverse("airport:airplane-list")


def airplane_sample(**kwargs) -> Airplane:
    default = {
        "name": "Airplane Sample",
        "rows": 4,
        "seats_in_row": 50,
    }
    default.update(kwargs)
    return Airplane.objects.create(**default)


def get_airplane_detail_url(pk: int) -> str:
    return reverse("airport:airplane-detail", kwargs={"pk": pk})


class UnauthenticatedAirplaneApiTests(APITestCase):

    def setUp(self) -> None:
        self.facility_1 = facility_sample()
        self.facility_2 = facility_sample(name="Facility Sample 2")
        self.airplane_type_1 = airplane_type_sample()
        self.airplane_type_2 = airplane_type_sample(
            name="Airplane Type Sample 2"
        )
        self.airplane_1 = airplane_sample(
            airplane_type_id=self.airplane_type_1.id,
        )
        self.airplane_2 = airplane_sample(
            name="Airplane Sample 2",
            airplane_type_id=self.airplane_type_2.id
        )
        self.airplane_1.facilities.add(self.facility_1)
        self.airplane_2.facilities.add(self.facility_2)

    def test_airplane_list(self) -> None:
        airplanes = (self.airplane_1, self.airplane_2)
        response = self.client.get(AIRPLANE_LIST_URL)
        serializer = AirplaneListRetrieveSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_airplane_list_filter_by_airplane_type(self) -> None:
        response = self.client.get(
            AIRPLANE_LIST_URL,
            query_params={"airplane_type_id": self.airplane_type_2.id}
        )
        serializer_airplane_1 = AirplaneListRetrieveSerializer(
            self.airplane_1
        )
        serializer_airplane_2 = AirplaneListRetrieveSerializer(
            self.airplane_2
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_airplane_1.data, response.data["results"])
        self.assertIn(serializer_airplane_2.data, response.data["results"])

    def test_airplane_list_filter_by_facilities(self) -> None:
        response = self.client.get(
            AIRPLANE_LIST_URL,
            query_params={"facilities": (self.facility_1.id,)}
        )
        serializer_airplane_1 = AirplaneListRetrieveSerializer(
            self.airplane_1
        )
        serializer_airplane_2 = AirplaneListRetrieveSerializer(
            self.airplane_2
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_airplane_1.data, response.data["results"])
        self.assertNotIn(serializer_airplane_2.data, response.data["results"])

    def test_airplane_list_with_pagination(self) -> None:
        PAGE_SIZE = 1
        response = self.client.get(
            AIRPLANE_LIST_URL,
            query_params={"page_size": PAGE_SIZE}
        )
        serializer_airplane_1 = AirplaneListRetrieveSerializer(
            self.airplane_1
        )
        serializer_airplane_2 = AirplaneListRetrieveSerializer(
            self.airplane_2
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_airplane_1.data, response.data["results"])
        self.assertNotIn(serializer_airplane_2.data, response.data["results"])

    def test_airplane_retrieve(self) -> None:
        URL = get_airplane_detail_url(pk=self.airplane_1.id)
        response = self.client.get(URL)
        serializer = AirplaneListRetrieveSerializer(self.airplane_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_airplane_create_authentication_required(self) -> None:
        data = {
            "name": "Test airplane",
            "rows": 2,
            "seats_in_row": 25,
            "airplane_type": self.airplane_type_1.id,
            "facilities": (self.facility_1.id, self.facility_2.id)
        }
        response = self.client.post(AIRPLANE_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_update_authentication_required(self) -> None:
        data = {
            "name": "Another test airplane",
            "rows": 5,
            "seats_in_row": 50
        }
        URL = get_airplane_detail_url(pk=self.airplane_1.id)
        response = self.client.put(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_partial_update_authentication_required(self) -> None:
        data = {"description": "Test description"}
        URL = get_airplane_detail_url(pk=self.airplane_1.id)
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_destroy_authentication_required(self) -> None:
        URL = get_airplane_detail_url(pk=self.airplane_1.id)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_upload_image_authentication_required(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            URL = get_airplane_detail_url(pk=self.airplane_1.id)
            image = Image.new("RGB", (25, 25))

            image.save(ntf, format="JPEG")
            ntf.seek(0)

            data = {"image": ntf}
            response = self.client.post(URL, data=data, format="multipart")

            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED
            )


class AuthenticatedAirplaneApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@airport.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)

    def test_airplane_create_is_forbidden(self) -> None:
        data = {
            "name": "Test airplane",
            "rows": 4,
            "seats_in_row": 30
        }
        response = self.client.post(AIRPLANE_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_update_is_forbidden(self) -> None:
        data = {
            "name": "Another test airplane",
            "rows": 2,
            "seats_in_row": 15
        }
        URL = get_airplane_detail_url(pk=1)
        response = self.client.put(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_partial_update_is_forbidden(self) -> None:
        data = {
            "description": "Test description",
            "rows": 10
        }
        URL = get_airplane_detail_url(pk=1)
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_destroy_is_forbidden(self) -> None:
        URL = get_airplane_detail_url(pk=1)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_upload_image_is_forbidden(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            URL = get_airplane_detail_url(pk=1)
            image = Image.new("RGB", (10, 10))

            image.save(ntf, format="JPEG")
            ntf.seek(0)

            data = {"image": ntf}
            response = self.client.post(URL, data=data, format="multipart")

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN
            )
