from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer


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

    def test_airplane_type_retrieve(self) -> None:
        airplane_type = airplane_type_sample()
        response = self.client.get(
            get_airplane_type_detail_url(airplane_type.id)
        )
        serializer = AirplaneTypeSerializer(airplane_type)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
