from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user.views import (
    RegisterUserAPIView,
    ManageUserAPIView,
    UserAdminViewSet
)


router = SimpleRouter()
router.register("accounts", UserAdminViewSet)


urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("me/", ManageUserAPIView.as_view(), name="manage"),
    path("", include(router.urls)),
]

app_name = "user"
