from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


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

    def test_route_create_authentication_required(self) -> None:
        data = {
            "source": 1,
            "destination": 2,
            "distance": 100
        }
        response = self.client.post(ROUTE_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_route_update_authentication_required(self) -> None:
        data = {
            "source": 2,
            "destination": 3,
            "distance": 250
        }
        url = get_route_detail_url(pk=1)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_route_partial_update_authentication_required(self) -> None:
        data = {"distance": 220}
        url = get_route_detail_url(pk=1)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_route_destroy_authentication_required(self) -> None:
        url = get_route_detail_url(pk=1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@airport.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)
