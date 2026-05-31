from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user.views import (
    CreateUserAPIView,
    ManageUserAPIView,
    UserViewSet
)


router = SimpleRouter()
router.register("", UserViewSet)


urlpatterns = [
    path("register/", CreateUserAPIView.as_view(), name="create"),
    path("me/", ManageUserAPIView.as_view(), name="manage")
]

app_name = "user"
