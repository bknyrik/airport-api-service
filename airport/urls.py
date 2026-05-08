from rest_framework.routers import DefaultRouter

from airport.views import (
    FacilityViewSet,
    AirplaneTypeViewSet
)


router = DefaultRouter()
router.register("facilities", FacilityViewSet)
router.register("airplane_types", AirplaneTypeViewSet)


urlpatterns = router.urls


app_name = "airport"
