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

    def test_facility_list(self) -> None:
        facilities = (
            facility_sample(),
            facility_sample(name="Test facility 2"),
            facility_sample(name="Test facility 3"),
        )
        response = self.client.get(FACILITY_LIST_URL)
        serializer = FacilitySerializer(facilities, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_facility_list_with_pagination(self) -> None:
        PAGE_SIZE = 2
        facility = facility_sample()
        facility2 = facility_sample(name="Test facility 2")
        facility3 = facility_sample(name="Test facility 3")

        response = self.client.get(
            FACILITY_LIST_URL,
            query_params={"page_size": PAGE_SIZE}
        )
        serializer = FacilitySerializer((facility, facility2), many=True)
        serializer_facility3 = FacilitySerializer(facility3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])
        self.assertNotIn(serializer_facility3.data, response.data["results"])

    def test_facility_retrieve(self) -> None:
        facility = facility_sample()
        response = self.client.get(get_facility_detail_url(pk=facility.id))
        serializer = FacilitySerializer(facility)

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
        response = self.client.put(get_facility_detail_url(pk=1), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_facility_partial_update_authentication_required(self) -> None:
        data = {"description": "updated description"}
        response = self.client.patch(get_facility_detail_url(pk=1), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_facility_destroy_authentication_required(self) -> None:
        response = self.client.delete(get_facility_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFacilityApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass12345"
        )
        self.client.force_authenticate(user=self.user)

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
        response = self.client.put(get_facility_detail_url(pk=1), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_facility_partial_update_is_forbidden(self) -> None:
        data = {"description": "Another description"}
        response = self.client.patch(get_facility_detail_url(pk=1), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_facility_destroy_is_forbidden(self) -> None:
        response = self.client.delete(get_facility_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedAdminFacilityApiTests(APITestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="adminpass12345",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

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

    def test_facility_update(self) -> None:
        facility = facility_sample()
        data = {
            "name": "Another facility name",
            "description": "Another facility description"
        }
        response = self.client.put(
            get_facility_detail_url(pk=facility.id),
            data=data
        )
        serializer = FacilitySerializer(facility)

        facility.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
