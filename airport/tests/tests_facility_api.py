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
