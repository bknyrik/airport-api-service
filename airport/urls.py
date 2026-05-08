from rest_framework.routers import DefaultRouter

from airport.views import FacilityViewSet


router = DefaultRouter()
router.register("facilities", FacilityViewSet)


urlpatterns = router.urls


app_name = "airport"
