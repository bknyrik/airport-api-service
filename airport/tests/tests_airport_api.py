import tempfile

from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from PIL import Image

from airport.models import Airport
from airport.serializers import AirportSerializer


User = get_user_model()


AIRPORT_LIST_URL = reverse("airport:airport-list")


def airport_sample(**kwargs) -> Airport:
    default = {
        "name": "Sample airport",
        "country": "Sample country",
        "city": "Sample city",
    }
    default.update(kwargs)
    return Airport.objects.create(**default)


def get_airport_detail_url(pk: int) -> str:
    return reverse("airport:airport-detail", kwargs={"pk": pk})


def get_airport_upload_image_url(pk: int) -> str:
    return reverse("airport:airport-upload-image", kwargs={"pk": pk})


class UnauthenticatedAirportApiTests(APITestCase):

    def test_airport_list_authentication_required(self) -> None:
        response = self.client.get(AIRPORT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_retrieve_authentication_required(self) -> None:
        response = self.client.get(get_airport_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_create_authentication_required(self) -> None:
        data = {
            "name": "Test Airport",
            "country": "Test country",
            "city": "Test city",
        }
        response = self.client.post(AIRPORT_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_update_authentication_required(self) -> None:
        data = {
            "name": "Another test airport",
            "country": "Another test country",
            "city": "Another test city"
        }
        response = self.client.put(
            get_airport_detail_url(pk=1),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_partial_update_authentication_required(self) -> None:
        data = {"iata_code": "TST"}
        response = self.client.patch(get_airport_detail_url(pk=1), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_destroy_authentication_required(self) -> None:
        response = self.client.delete(get_airport_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_upload_image_authentication_required(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            image = Image.new("RGB", (25, 25))
            image.save(ntf, format="JPEG")
            image.seek(0)

            response = self.client.post(
                get_airport_upload_image_url(pk=1),
                data={"image": ntf},
                format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@test.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)

    def test_airport_list(self) -> None:
        airports = (
            airport_sample(),
            airport_sample(name="Sample airport 2"),
            airport_sample(name="Sample airport 3"),
        )
        response = self.client.get(AIRPORT_LIST_URL)
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_airport_list_filter_by_country(self) -> None:
        COUNTRY = "Germany"
        airport = airport_sample(country="Germany")
        airport2 = airport_sample(name="Sample airport 2", country="Germany")
        airport3 = airport_sample(name="Sample airport 3", country="France")
        response = self.client.get(
            AIRPORT_LIST_URL,
            query_params={"country": COUNTRY}
        )
        airports_with_germany_serializer = AirportSerializer(
            (airport, airport2),
            many=True
        )
        airport_with_france_serializer = AirportSerializer(airport3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            airports_with_germany_serializer.data,
            response.data["results"]
        )
        self.assertNotIn(
            airport_with_france_serializer.data,
            response.data["results"]
        )

    def test_airport_list_filter_by_city(self) -> None:
        CITY = "Paris"
        airport = airport_sample(city="Paris")
        airport2 = airport_sample(city="Berlin")
        airport3 = airport_sample(name="France airport", city="Paris")
        response = self.client.get(
            AIRPORT_LIST_URL,
            query_params={"city": CITY}
        )
        airports_with_paris_serializer = AirportSerializer(
            (airport, airport3),
            many=True
        )
        airport_with_berlin_serializer = AirportSerializer(airport2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            airports_with_paris_serializer.data,
            response.data["results"]
        )
        self.assertNotIn(
            airport_with_berlin_serializer.data,
            response.data["results"]
        )
