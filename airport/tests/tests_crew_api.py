from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


CREW_LIST_URL = reverse("airport:crew-list")


class UnauthenticatedCrewApiTests(APITestCase):

    def test_crew_list_authentication_required(self) -> None:
        response = self.client.get(CREW_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
