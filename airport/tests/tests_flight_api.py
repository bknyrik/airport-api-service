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
