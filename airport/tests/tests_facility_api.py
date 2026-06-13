from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from airport.serializers import FacilitySerializer
from airport.models import Facility


User = get_user_model()


FACILITY_LIST_URL = reverse("airport:facility-list")


def facility_sample(**kwargs) -> Facility:
    defaults = {
        "name": "Test facility",
        "description": "Test description"
    }
    defaults.update(kwargs)
    return Facility.objects.create(**defaults)


def get_facility_detail_url(pk: int) -> str:
    return reverse("airport:facility-detail", kwargs={"pk": pk})


class UnauthenticatedFacilityApiTests(APITestCase):

    def setUp(self) -> None:
        self.facility_1 = facility_sample()
        self.facility_2 = facility_sample(name="Test facility 2")
        self.facility_3 = facility_sample(name="Test facility 3")

    def test_facility_list(self) -> None:
        response = self.client.get(FACILITY_LIST_URL)
        serializer = FacilitySerializer(
            (self.facility_1, self.facility_2, self.facility_3),
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_facility_list_with_pagination(self) -> None:
        PAGE_SIZE = 2

        response = self.client.get(
            FACILITY_LIST_URL,
            query_params={"page_size": PAGE_SIZE}
        )
        serializer_facility_1_and_2 = FacilitySerializer(
            (self.facility_1, self.facility_2),
            many=True
        )
        serializer_facility3 = FacilitySerializer(self.facility_3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            serializer_facility_1_and_2.data,
            response.data["results"]
        )
        self.assertNotIn(serializer_facility3.data, response.data["results"])

    def test_facility_retrieve(self) -> None:
        URL = get_facility_detail_url(pk=self.facility_1.id)
        response = self.client.get(URL)
        serializer = FacilitySerializer(self.facility_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_facility_create_authentication_required(self) -> None:
        data = {"name": "Test facility"}
        response = self.client.post(FACILITY_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_facility_update_authentication_required(self) -> None:
        data = {
            "name": "Updated test facility",
            "description": "Updated description"
        }
        URL = get_facility_detail_url(pk=1)
        response = self.client.put(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_facility_partial_update_authentication_required(self) -> None:
        data = {"description": "updated description"}
        URL = get_facility_detail_url(pk=1)
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_facility_destroy_authentication_required(self) -> None:
        URL = get_facility_detail_url(pk=1)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFacilityApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass12345"
        )
        self.client.force_authenticate(user=self.user)
        self.facility = facility_sample()

    def test_facility_create_is_forbidden(self) -> None:
        data = {
            "name": "Test facility",
            "description": "Test description"
        }
        response = self.client.post(FACILITY_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_facility_update_is_forbidden(self) -> None:
        data = {
            "name": "Another facility",
            "description": "Another description"
        }
        URL = get_facility_detail_url(pk=1)
        response = self.client.put(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_facility_partial_update_is_forbidden(self) -> None:
        data = {"description": "Another description"}
        URL = get_facility_detail_url(pk=1)
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_facility_destroy_is_forbidden(self) -> None:
        URL = get_facility_detail_url(pk=1)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFacilityApiTests(APITestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="adminpass12345",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)
        self.facility = facility_sample()

    def test_facility_create(self) -> None:
        data = {
            "name": "Facility",
            "description": "Description"
        }
        response = self.client.post(FACILITY_LIST_URL, data=data)
        serializer = FacilitySerializer(
            Facility.objects.get(name=data["name"])
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_facility_create_has_bad_request(self) -> None:
        data = {"name": self.facility.name}
        response = self.client.post(FACILITY_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_facility_update(self) -> None:
        data = {
            "name": "Another facility name",
            "description": "Another facility description"
        }
        URL = get_facility_detail_url(pk=self.facility.id)
        response = self.client.put(URL, data=data)
        serializer = FacilitySerializer(self.facility)

        self.facility.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_facility_update_has_bad_request(self) -> None:
        another_facility = facility_sample(name="Another facility")
        URL = get_facility_detail_url(pk=self.facility.id)
        data = {"name": another_facility.name}
        response = self.client.put(URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_facility_partial_update(self) -> None:
        data = {"description": "Another description"}
        URL = get_facility_detail_url(pk=self.facility.id)
        response = self.client.patch(URL, data=data)
        serializer = FacilitySerializer(self.facility)

        self.facility.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_facility_partial_update_has_bad_request(self) -> None:
        another_facility = facility_sample(name="Another facility")
        URL = get_facility_detail_url(pk=self.facility.id)
        data = {"name": another_facility.name}
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_facility_destroy(self) -> None:
        URL = get_facility_detail_url(pk=self.facility.id)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Facility.objects.filter(pk=self.facility.id).exists()
        )
