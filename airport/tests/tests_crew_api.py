from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import Crew
from airport.serializers import CrewListRetrieveSerializer


User = get_user_model()


CREW_LIST_URL = reverse("airport:crew-list")


def crew_sample(**kwargs) -> Crew:
    default = {
        "first_name": "John",
        "last_name": "Doe",
        "role": Crew.Role.COMMANDER
    }
    default.update(kwargs)
    return Crew.objects.create(**default)


def get_crew_detail_url(pk: int) -> str:
    return reverse("airport:crew-detail", kwargs={"pk": pk})



class UnauthenticatedCrewApiTests(APITestCase):

    def test_crew_list_authentication_required(self) -> None:
        response = self.client.get(CREW_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_retrieve_authentication_required(self) -> None:
        response = self.client.get(get_crew_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_create_authentication_required(self) -> None:
        data = {"first_name": "John", "last_name": "Doe", "role": "CP"}
        response = self.client.post(CREW_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_update_authentication_required(self) -> None:
        data = {
            "first_name": "Updated first",
            "last_name": "Updated last",
            "role": "CM"
        }
        response = self.client.put(get_crew_detail_url(pk=1), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_partial_update_authentication_required(self) -> None:
        data = {"first_name": "Update first", "role": "FA"}
        response = self.client.patch(get_crew_detail_url(pk=1), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_destroy_authentication_required(self) -> None:
        response = self.client.delete(get_crew_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@test.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)

    def test_crew_list(self) -> None:
        crew_sample()
        crew_sample()
        crew_sample()

        response = self.client.get(CREW_LIST_URL)
        serializer = CrewListRetrieveSerializer(Crew.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])
