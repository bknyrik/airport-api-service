from datetime import datetime

from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


FLIGHT_LIST_URL = reverse("airport:flight-list")


def get_flight_detail_url(pk: int) -> str:
    return reverse("airport:flight-detail", kwargs={"pk": pk})


class UnauthenticatedFlightApiTests(APITestCase):

    def test_flight_list_authentication_required(self) -> None:
        response = self.client.get(FLIGHT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_retrieve_authentication_required(self) -> None:
        url = get_flight_detail_url(pk=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_create_authentication_required(self) -> None:
        data = {
            "route": 1,
            "airplane": 1,
            "departure_time": datetime(year=2026, month=1, day=1),
            "arrival_time": datetime(year=2026, month=2, day=4),
            "crewmembers": (1, 2, 3)
        }
        response = self.client.post(FLIGHT_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_update_authentication_required(self) -> None:
        data = {
            "route": 2,
            "airplane": 3,
            "departure_time": datetime(year=2026, month=1, day=10),
            "arrival_time": datetime(year=2026, month=1, day=15),
        }
        url = get_flight_detail_url(pk=1)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_partial_update_authentication_required(self) -> None:
        data = {
            "route": 1,
            "airplane": 4,
        }
        url = get_flight_detail_url(pk=1)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
