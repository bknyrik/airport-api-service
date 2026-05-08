from rest_framework.routers import DefaultRouter

from airport.views import (
    FacilityViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet
)


router = DefaultRouter()
router.register("facilities", FacilityViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)


urlpatterns = router.urls


app_name = "airport"
