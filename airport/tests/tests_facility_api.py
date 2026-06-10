from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from airport.serializers import FacilitySerializer
from airport.models import Facility


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
