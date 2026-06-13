from datetime import datetime

from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.db.models import F, Count
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import Flight
from airport.serializers import (
    FlightListRetrieveSerializer,
    FlightSerializer
)
from airport.tests.tests_airport_api import airport_sample
from airport.tests.tests_route_api import route_sample
from airport.tests.tests_airplane_api import airplane_sample
from airport.tests.tests_facility_api import facility_sample
from airport.tests.tests_airplane_type_api import airplane_type_sample
from airport.tests.tests_crew_api import crew_sample


User = get_user_model()


FLIGHT_LIST_URL = reverse("airport:flight-list")


def get_flight_detail_url(pk: int) -> str:
    return reverse("airport:flight-detail", kwargs={"pk": pk})


def flight_sample(**kwargs) -> Flight:
    defaults = {
        "departure_time": datetime(year=2026, month=2, day=1),
        "arrival_time": datetime(year=2026, month=2, day=5),
    }
    defaults.update(kwargs)
    return Flight.objects.create(**defaults)


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

    def test_flight_destroy_authentication_required(self) -> None:
        url = get_flight_detail_url(pk=1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@airport.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)

        self.airplane_type = airplane_type_sample()
        self.facility = facility_sample()

        self.airplane_1 = airplane_sample(
            airplane_type_id=self.airplane_type.id
        )
        self.airplane_2 = airplane_sample(
            name="Airplane Sample 2",
            airplane_type_id=self.airplane_type.id
        )
        self.airplane_1.facilities.add(self.facility)
        self.airplane_2.facilities.add(self.facility)

        self.airport_1 = airport_sample()
        self.airport_2 = airport_sample(
            name="Airport Sample 2",
        )
        self.airport_3 = airport_sample(
            name="Airport Sample 3"
        )

        self.route_1 = route_sample(
            source_id=self.airport_1.id,
            destination_id=self.airport_2.id
        )
        self.route_2 = route_sample(
            source_id=self.airport_2.id,
            destination_id=self.airport_3.id
        )
        self.crew_1 = crew_sample()
        self.crew_2 = crew_sample()

        self.flight_1 = flight_sample(
            route_id=self.route_1.id,
            airplane_id=self.airplane_1.id
        )
        self.flight_2 = flight_sample(
            route_id=self.route_2.id,
            airplane_id=self.airplane_2.id
        )
        self.flight_1.crewmembers.add(self.crew_1)
        self.flight_2.crewmembers.add(self.crew_2)
        flights = Flight.objects.annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )
        self.flight_1 = flights.get(pk=self.flight_1.id)
        self.flight_2 = flights.get(pk=self.flight_2.id)

    def test_flight_list(self) -> None:
        flights = (self.flight_1, self.flight_2)
        response = self.client.get(FLIGHT_LIST_URL)
        serializer = FlightListRetrieveSerializer(
            flights,
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_flight_list_filter_by_route_id(self) -> None:
        ROUTE_ID = self.route_1.id
        response = self.client.get(
            FLIGHT_LIST_URL,
            query_params={"route_id": ROUTE_ID}
        )
        serializer_flight_match_route_id = (
            FlightListRetrieveSerializer(self.flight_1)
        )
        serializer_flight_doesnt_match_route_id = (
            FlightListRetrieveSerializer(self.flight_2)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            serializer_flight_match_route_id.data,
            response.data["results"]
        )
        self.assertNotIn(
            serializer_flight_doesnt_match_route_id.data,
            response.data["results"]
        )

    def test_flight_list_filter_by_airplane_id(self) -> None:
        AIRPLANE_ID = self.airplane_2.id
        response = self.client.get(
            FLIGHT_LIST_URL,
            query_params={"airplane_id": AIRPLANE_ID}
        )
        serializer_flight_doesnt_match_airplane_id = (
            FlightListRetrieveSerializer(self.flight_1)
        )
        serializer_flight_match_airplane_id = (
            FlightListRetrieveSerializer(self.flight_2)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(
            serializer_flight_doesnt_match_airplane_id.data,
            response.data["results"]
        )
        self.assertIn(
            serializer_flight_match_airplane_id.data,
            response.data["results"]
        )

    def test_flight_list_filter_by_crewmembers_ids(self) -> None:
        CREWMEMBERS_IDS = (self.crew_1.id, )
        response = self.client.get(
            FLIGHT_LIST_URL,
            query_params={"crewmembers": CREWMEMBERS_IDS}
        )
        serializer_flight_match_crewmembers = (
            FlightListRetrieveSerializer(self.flight_1)
        )
        serializer_flight_doesnt_match_crewmembers = (
            FlightListRetrieveSerializer(self.flight_2)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            serializer_flight_match_crewmembers.data,
            response.data["results"]
        )
        self.assertNotIn(
            serializer_flight_doesnt_match_crewmembers.data,
            response.data["results"]
        )

    def test_flight_retrieve(self) -> None:
        url = get_flight_detail_url(pk=self.flight_1.id)
        response = self.client.get(url)
        serializer = FlightListRetrieveSerializer(self.flight_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_flight_create_is_forbidden(self) -> None:
        data = {
            "route": self.route_2.id,
            "airplane": self.airplane_1.id,
            "departure_time": datetime(2026, 5, 1),
            "arrival_time": datetime(2026, 5, 10),
        }
        response = self.client.post(FLIGHT_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flight_update_is_forbidden(self) -> None:
        data = {
            "route": self.route_1.id,
            "airplane": self.airplane_2.id,
            "departure_time": datetime(2026, 1, 10),
            "arrival_time": datetime(2026, 1, 15),
        }
        url = get_flight_detail_url(pk=self.flight_2.id)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flight_partial_update_is_forbidden(self) -> None:
        data = {"airplane": self.airplane_1.id}
        url = get_flight_detail_url(pk=self.flight_2.id)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flight_destroy_is_forbidden(self) -> None:
        url = get_flight_detail_url(pk=self.flight_1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(APITestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            email="admin@airport.com",
            password="admin12345",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)
        self.airplane_type = airplane_type_sample()
        self.facility = facility_sample()

        self.airplane_1 = airplane_sample(
            airplane_type_id=self.airplane_type.id,
        )
        self.airplane_2 = airplane_sample(
            name="Airplane Sample 2",
            airplane_type_id=self.airplane_type.id
        )
        self.airplane_1.facilities.add(self.facility)
        self.airplane_2.facilities.add(self.facility)

        self.airport_1 = airport_sample()
        self.airport_2 = airport_sample(name="Airport Sample 2")

        self.crew_1 = crew_sample()
        self.crew_2 = crew_sample()
        self.route_1 = route_sample(
            source_id=self.airport_1.id,
            destination_id=self.airport_2.id,
        )
        self.route_2 = route_sample(
            source_id=self.airport_2.id,
            destination_id=self.airport_1.id
        )

        self.flight = flight_sample(
            airplane_id=self.airplane_2.id,
            route_id=self.route_1.id
        )
        self.flight.crewmembers.add(self.crew_1)

    def test_flight_create(self) -> None:
        data = {
            "route": self.route_2.id,
            "airplane": self.airplane_2.id,
            "departure_time": datetime(2026, 1, 2),
            "arrival_time": datetime(2026, 1, 5),
            "crewmembers": (self.crew_1.id,)
        }
        response = self.client.post(FLIGHT_LIST_URL, data=data)
        flight = Flight.objects.get(**data)
        serializer = FlightSerializer(flight)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_flight_create_has_bad_request(self) -> None:
        data = {
            "route": 999,
            "airplane": 999,
            "departure_time": "not a date",
            "arrival_time": datetime(2026, 4, 20),
            "crewmembers": (self.crew_2.id,)
        }
        response = self.client.post(FLIGHT_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_flight_update(self) -> None:
        data = {
            "route": self.route_2.id,
            "airplane": self.airplane_2.id,
            "departure_time": datetime(2026, 3, 3),
            "arrival_time": datetime(2026, 3, 10),
            "crewmembers": (self.crew_1.id, self.crew_2.id)
        }
        url = get_flight_detail_url(pk=self.flight.id)
        response = self.client.put(url, data=data)
        serializer = FlightSerializer(self.flight)

        self.flight.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_flight_update_has_bad_request(self) -> None:
        data = {
            "route": self.route_2.id,
            "airplane": self.airplane_2.id,
            "departure_time": datetime(2026, 4, 1),
            "arrival_time": datetime(2026, 3, 29),
            "crewmembers": (self.crew_2.id,)
        }
        url = get_flight_detail_url(pk=self.flight.id)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
