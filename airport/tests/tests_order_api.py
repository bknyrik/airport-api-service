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
