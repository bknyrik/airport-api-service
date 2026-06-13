from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


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
