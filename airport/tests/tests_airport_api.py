from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


AIRPORT_LIST_URL = reverse("airport:airport-list")


def get_airport_detail_url(pk: int) -> str:
    return reverse("airport:airport-detail", kwargs={"pk": pk})


class UnauthenticatedAirportApiTests(APITestCase):

    def test_airport_list_authentication_required(self) -> None:
        response = self.client.get(AIRPORT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_retrieve_authentication_required(self) -> None:
        response = self.client.get(get_airport_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
