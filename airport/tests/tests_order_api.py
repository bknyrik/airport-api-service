from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import Order, Ticket
from airport.serializers import (
    OrderSerializer,
    OrderListRetrieveSerializer
)
from airport.tests.tests_airport_api import airport_sample
from airport.tests.tests_airplane_type_api import airplane_type_sample
from airport.tests.tests_airplane_api import airplane_sample
from airport.tests.tests_facility_api import facility_sample
from airport.tests.tests_route_api import route_sample
from airport.tests.tests_crew_api import crew_sample
from airport.tests.tests_flight_api import flight_sample


User = get_user_model()


ORDER_LIST_URL = reverse("airport:order-list")


def get_order_detail_url(pk: int) -> str:
    return reverse("airport:order-detail", kwargs={"pk": pk})


class UnauthenticatedOrderApiTests(APITestCase):

    def test_order_list_authentication_required(self) -> None:
        response = self.client.get(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_retrieve_authentication_required(self) -> None:
        url = get_order_detail_url(pk=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_create_authentication_required(self) -> None:
        data = {
            "tickets": (
                {
                    "flight": 1,
                    "row": 1,
                    "seat": 1
                },
            )
        }
        response = self.client.post(ORDER_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_update_authentication_required(self) -> None:
        data = {
            "tickets": (
                {
                    "flight": 2,
                    "row": 2,
                    "seat": 2
                },
            )
        }
        url = get_order_detail_url(pk=1)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_partial_update_authentication_required(self) -> None:
        data = {
            "tickets": (
                {
                    "flight": 4,
                    "row": 2
                }
            )
        }
        url = get_order_detail_url(pk=1)
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_destroy_authentication_required(self) -> None:
        url = get_order_detail_url(pk=1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@airport.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)

        self.airplane_type = airplane_type_sample()
        self.facility = facility_sample()
        self.airplane = airplane_sample(
            airplane_type_id=self.airplane_type.id
        )
        self.airplane.facilities.add(self.facility)

        self.airport_1 = airport_sample()
        self.airport_2 = airport_sample(name="Airport Sample 2")

        self.route = route_sample(
            source_id=self.airport_1.id,
            destination_id=self.airport_2.id,
        )
        self.crew = crew_sample()

        self.flight = flight_sample(
            route_id=self.route.id,
            airplane_id=self.airplane.id,
        )
        self.flight.crewmembers.add(self.crew)
        self.order = Order.objects.create(
            user_id=self.user.id
        )
        self.order_2 = Order.objects.create(
            user_id=self.user.id
        )
        self.ticket_1 = Ticket.objects.create(
            flight_id=self.flight.id,
            row=1,
            seat=1,
            order_id=self.order.id
        )
        self.ticket_2 = Ticket.objects.create(
            flight_id=self.flight.id,
            row=1,
            seat=2,
            order_id=self.order.id
        )
        self.ticket_3 = Ticket.objects.create(
            flight_id=self.flight.id,
            row=4,
            seat=1,
            order_id=self.order_2.id
        )

    def test_order_list(self) -> None:
        response = self.client.get(ORDER_LIST_URL)
        serializer = OrderListRetrieveSerializer(
            Order.objects.all(),
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_order_list_with_pagination(self) -> None:
        PAGE_SIZE = 1
        response = self.client.get(
            ORDER_LIST_URL,
            query_params={"page_size": PAGE_SIZE}
        )
        serializer_order_1 = OrderListRetrieveSerializer(self.order)
        serializer_order_2 = OrderListRetrieveSerializer(self.order_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_order_1.data, response.data["results"])
        self.assertNotIn(serializer_order_2.data, response.data["results"])

    def test_order_create(self) -> None:
        data = {
            "tickets": (
                {
                    "flight": self.flight.id,
                    "row": 2,
                    "seat": 3
                },
                {
                    "flight": self.flight.id,
                    "row": 3,
                    "seat": 4
                }
            )
        }
        response = self.client.post(ORDER_LIST_URL, data=data, format="json")
        order = Order.objects.get(
            tickets__flight=data["tickets"][0]["flight"],
            tickets__row=data["tickets"][0]["row"],
            tickets__seat=data["tickets"][0]["seat"],
        )
        serializer = OrderSerializer(order)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_order_create_has_bad_request(self) -> None:
        data = {
            "tickets": (
                {
                    "flight": self.flight.id,
                    "row": 1,
                    "seat": 1,
                },
                {
                    "flight": self.flight.id,
                    "row": 999,
                    "seat": 999
                }
            )
        }
        response = self.client.post(ORDER_LIST_URL, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_update(self) -> None:
        data = {
            "tickets": (
                {
                    "flight": self.flight.id,
                    "row": 2,
                    "seat": 2
                },
                {
                    "flight": self.flight.id,
                    "row": 2,
                    "seat": 3
                },
                {
                    "flight": self.flight.id,
                    "row": 2,
                    "seat": 4
                }
            )
        }
        url = get_order_detail_url(pk=self.order.id)
        response = self.client.put(url, data=data, format="json")
        serializer = OrderSerializer(self.order)

        self.order.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_order_update_has_bad_request(self) -> None:
        data = {
            "tickets": (
                {
                    "flight": 999,
                    "row": 1,
                    "seat": 1
                },
                {
                    "flight": self.flight.id,
                    "row": 1,
                    "seat": 2,
                }
            )
        }
        url = get_order_detail_url(pk=self.order.id)
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_partial_update(self) -> None:
        data = {
            "tickets": (
                {
                    "id": self.ticket_1.id,
                    "flight": self.ticket_1.flight.id,
                    "row": 2,
                    "seat": 3
                },
            )
        }
        url = get_order_detail_url(pk=self.order.id)
        response = self.client.patch(url, data=data, format="json")
        serializer = OrderSerializer(self.order)

        self.order.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_order_partial_update_has_bad_request(self) -> None:
        data = {
            "tickets": (
                {
                    "id": self.ticket_2.id,
                    "flight": self.ticket_2.flight.id,
                    "row": 1,
                    "seat": 2,
                },
                {
                    "id": self.ticket_1.id,
                    "flight": self.ticket_1.flight.id,
                    "row": 1,
                    "seat": 2,
                }
            )
        }
        url = get_order_detail_url(pk=self.order.id)
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_destroy(self) -> None:
        url = get_order_detail_url(pk=self.order.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.id).exists())
        self.assertFalse(Ticket.objects.filter(pk=self.ticket_1.id).exists())
        self.assertFalse(Ticket.objects.filter(pk=self.ticket_2.id).exists())
