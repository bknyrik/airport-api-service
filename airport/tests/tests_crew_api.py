from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from airport.models import Crew
from airport.serializers import CrewListRetrieveSerializer, CrewSerializer


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
        URL = get_crew_detail_url(pk=1)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@test.com",
            password="userpass12345"
        )
        self.client.force_authenticate(user=self.user)
        self.crew_1 = crew_sample(
            first_name="Aaron"
        )
        self.crew_2 = crew_sample(
            first_name="Mark",
            last_name="Adamson",
            role=Crew.Role.COPILOT
        )
        self.crew_3 = crew_sample(
            first_name="Leon",
            last_name="Anderson",
            role=Crew.Role.COPILOT
        )

    def test_crew_list(self) -> None:
        crewmembers = (self.crew_1, self.crew_2, self.crew_3)
        response = self.client.get(CREW_LIST_URL)
        serializer = CrewListRetrieveSerializer(crewmembers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data["results"])

    def test_crew_list_filter_by_role(self) -> None:
        ROLE = "CP"
        response = self.client.get(CREW_LIST_URL, query_params={"role": ROLE})

        serializer_copilots = CrewListRetrieveSerializer(
            (self.crew_2, self.crew_3),
            many=True
        )
        serializer_commander = CrewListRetrieveSerializer(self.crew_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_copilots.data, response.data["results"])
        self.assertNotIn(serializer_commander.data, response.data["results"])

    def test_crew_list_filter_by_first_name(self) -> None:
        FIRST_NAME = "on"
        response = self.client.get(
            CREW_LIST_URL,
            query_params={"first_name": FIRST_NAME}
        )

        serializer_crew_match_first_name = CrewListRetrieveSerializer(
            (self.crew_1, self.crew_3),
            many=True
        )
        serializer_crew_not_match_first_name = CrewListRetrieveSerializer(
            self.crew_2
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            serializer_crew_match_first_name.data,
            response.data["results"]
        )
        self.assertNotIn(
            serializer_crew_not_match_first_name.data,
            response.data["results"]
        )

    def test_crew_list_filter_by_last_name(self) -> None:
        LAST_NAME = "son"

        response = self.client.get(
            CREW_LIST_URL,
            query_params={"last_name": LAST_NAME}
        )

        serializer_crew_match_last_name = CrewListRetrieveSerializer(
            (self.crew_2, self.crew_3),
            many=True
        )
        serializer_crew_not_match_last_name = CrewListRetrieveSerializer(
            self.crew_1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            serializer_crew_match_last_name.data,
            response.data["results"]
        )
        self.assertNotIn(
            serializer_crew_not_match_last_name.data,
            response.data["results"]
        )

    def test_crew_retrieve(self) -> None:
        URL = get_crew_detail_url(pk=self.crew_1.id)
        response = self.client.get(URL)
        serializer = CrewListRetrieveSerializer(self.crew_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_crew_create_is_forbidden(self) -> None:
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "role": "CP",
        }
        response = self.client.post(CREW_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_update_is_forbidden(self) -> None:
        data = {
            "first_name": "Updated first",
            "last_name": "Updated last",
            "role": "CP",
        }
        URL = get_crew_detail_url(pk=self.crew_1.id)
        response = self.client.put(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_partial_update_is_forbidden(self) -> None:
        data = {"role": "CM"}
        URL = get_crew_detail_url(pk=self.crew_1.id)
        response = self.client.patch(URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_destroy_is_forbidden(self) -> None:
        URL = get_crew_detail_url(pk=self.crew_1.id)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedAdminCrewApiTests(APITestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="adminpass12345",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)
        self.crew = crew_sample()

    def test_crew_create(self) -> None:
        data = {
            "first_name": "Test first",
            "last_name": "Test last",
            "role": "CP",
        }
        response = self.client.post(CREW_LIST_URL, data=data)
        crew = Crew.objects.get(**data)
        serializer = CrewSerializer(crew)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_crew_create_has_bad_request(self) -> None:
        data = {
            "first_name": "Test first",
            "last_name": "Test last",
            "role": "XX",
        }
        response = self.client.post(CREW_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crew_update(self) -> None:
        data = {
            "first_name": "Updated John",
            "last_name": "Updated Doe",
            "role": "CP",
        }
        response = self.client.put(
            get_crew_detail_url(pk=self.crew.id),
            data=data
        )
        serializer = CrewSerializer(self.crew)

        self.crew.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_crew_update_has_bad_request(self) -> None:
        data = {
            "first_name": "Updated John",
            "last_name": "Updated Doe",
            "role": "XX"
        }
        response = self.client.put(
            get_crew_detail_url(pk=self.crew.id),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crew_partial_update(self) -> None:
        data = {"role": "CP"}
        response = self.client.patch(
            get_crew_detail_url(pk=self.crew.id),
            data=data
        )
        serializer = CrewSerializer(self.crew)

        self.crew.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_crew_partial_update_has_bad_request(self) -> None:
        data = {"role": "DD"}
        response = self.client.patch(
            get_crew_detail_url(pk=self.crew.id),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crew_destroy(self) -> None:
        response = self.client.delete(get_crew_detail_url(pk=self.crew.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Crew.objects.filter(pk=self.crew.id).exists())
