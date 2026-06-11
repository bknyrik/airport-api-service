from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


CREW_LIST_URL = reverse("airport:crew-list")


def get_crew_detail_url(pk: int) -> str:
    return reverse("airport:crew-detail", kwargs={"pk": pk})



class UnauthenticatedCrewApiTests(APITestCase):

    def test_crew_list_authentication_required(self) -> None:
        response = self.client.get(CREW_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_retrieve_authentication_required(self) -> None:
        response = self.client.get(get_crew_detail_url(pk=1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
