from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import Route, Airport
from airport.serializers import RouteListRetrieveSerializer
from airport.tests.tests_airport_api import airport_sample


User = get_user_model()


ROUTE_LIST_URL = reverse("airport:route-list")


def get_route_detail_url(pk: int) -> str:
    return reverse("airport:route-detail", kwargs={"pk": pk})


def route_sample(**kwargs) -> Route:
    default = {
        "distance": 250
    }
    default.update(kwargs)
    return Route.objects.create(**default)


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
        self.airport_1 = airport_sample()
        self.airport_2 = airport_sample(
            name="Airport Sample 2"
        )
        self.airport_3 = airport_sample(
            name="Airport Sample 3"
        )
        self.route_1 = route_sample(
            source_id=self.airport_1.id,
            destination_id=self.airport_2.id,
        )
        self.route_2 = route_sample(
            source_id=self.airport_2.id,
            destination_id=self.airport_3.id,
            distance=500
        )
        self.client.force_authenticate(user=self.user)

    def test_route_list(self) -> None:
        response = self.client.get(ROUTE_LIST_URL)
        serializer = RouteListRetrieveSerializer(
            Route.objects.all(),
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_route_list_filter_by_min_distance(self) -> None:
        MIN_DISTANCE = 260
        response = self.client.get(
            ROUTE_LIST_URL,
            query_params={"min_distance": MIN_DISTANCE}
        )
        serializer_route_1 = RouteListRetrieveSerializer(self.route_1)
        serializer_route_2 = RouteListRetrieveSerializer(self.route_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_route_1.data, response.data["results"])
        self.assertIn(serializer_route_2.data, response.data["results"])
