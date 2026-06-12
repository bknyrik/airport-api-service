from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


ROUTE_LIST_URL = reverse("airport:route-list")


class UnauthenticatedRouteApiTests(APITestCase):

    def test_route_list_authentication_required(self) -> None:
        response = self.client.get(ROUTE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
