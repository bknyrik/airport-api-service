from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


ROUTE_LIST_URL = reverse("airport:route-list")


def get_route_detail_url(pk: int) -> str:
    return reverse("airport:route-detail", kwargs={"pk": pk})


class UnauthenticatedRouteApiTests(APITestCase):

    def test_route_list_authentication_required(self) -> None:
        response = self.client.get(ROUTE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_route_retrieve_authentication_required(self) -> None:
        url = get_route_detail_url(pk=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
