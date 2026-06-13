from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


ORDER_LIST_URL = reverse("airport:order-list")


class UnauthenticatedOrderApiTests(APITestCase):

    def test_order_list_authentication_required(self) -> None:
        response = self.client.get(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
