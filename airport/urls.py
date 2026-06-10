from rest_framework.routers import DefaultRouter

from airport.views import (
    FacilityViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    CrewViewSet,
    RouteViewSet,
    FlightViewSet,
    OrderViewSet
)


router = DefaultRouter()
router.register("facilities", FacilityViewSet)
router.register("airplane_types", AirplaneTypeViewSet, basename="airplane-type")
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("crewmembers", CrewViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)


urlpatterns = router.urls


app_name = "airport"
