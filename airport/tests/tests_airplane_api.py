from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import Airplane
from airport.serializers import AirplaneListRetrieveSerializer
from airport.tests.tests_airplane_type_api import airplane_type_sample
from airport.tests.tests_facility_api import facility_sample


AIRPLANE_LIST_URL = reverse("airport:airplane-list")


def airplane_sample(**kwargs) -> Airplane:
    default = {
        "name": "Airplane Sample",
        "rows": 4,
        "seats_in_row": 50,
    }
    default.update(kwargs)
    return Airplane.objects.create(**default)


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
