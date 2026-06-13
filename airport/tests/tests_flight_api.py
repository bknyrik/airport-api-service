from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


FLIGHT_LIST_URL = reverse("airport:flight-list")


class UnauthenticatedFlightApiTests(APITestCase):

    def test_flight_list_authentication_required(self) -> None:
        response = self.client.get(FLIGHT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
