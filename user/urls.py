from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user.views import (
    RegisterUserAPIView,
    ManageUserAPIView,
    UserAdminViewSet
)


router = SimpleRouter()
router.register("", UserAdminViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterUserAPIView.as_view(), name="create"),
    path("me/", ManageUserAPIView.as_view(), name="manage")
]

app_name = "user"
