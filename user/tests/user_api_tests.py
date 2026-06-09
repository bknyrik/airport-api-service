from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class UnauthenticatedUserApiTests(APITestCase):

    def test_user_admin_list_login_required(self) -> None:
        url = reverse("user:user-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
