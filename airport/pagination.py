from rest_framework.pagination import PageNumberPagination


class BaseSetPagination(PageNumberPagination):
    page_size_query_param = "page_size"


class FacilitySetPagination(BaseSetPagination):
    page_size = 15
    max_page_size = 25


class AirplaneTypeSetPagination(BaseSetPagination):
    page_size = 15
    max_page_size = 30


class AirplaneSetPagination(BaseSetPagination):
    page_size = 5
    max_page_size = 15


class AirportSetPagination(BaseSetPagination):
    page_size = 10
    max_page_size = 30


class CrewSetPagination(BaseSetPagination):
    page_size = 15
    max_page_size = 30


class RouteSetPagination(BaseSetPagination):
    page_size = 10
    max_page_size = 20


class FlightSetPagination(BaseSetPagination):
    page_size = 5
    max_page_size = 10


class OrderSetPagination(BaseSetPagination):
    page_size = 5
    max_page_size = 15
