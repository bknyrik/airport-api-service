from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


AIRPORT_LIST_URL = reverse("airport:airport-list")


class UnauthenticatedAirportApiTests(APITestCase):

    def test_airport_list_authentication_required(self) -> None:
        response = self.client.get(AIRPORT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
