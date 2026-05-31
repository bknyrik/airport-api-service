from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

from user.views import (
    RegisterUserAPIView,
    ManageUserAPIView,
    UserAdminViewSet
)


router = SimpleRouter()
router.register("", UserAdminViewSet)


urlpatterns = [
    path("token/obtain/", TokenObtainPairView.as_view(), name="token_obtain"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path("register/", RegisterUserAPIView.as_view(), name="create"),
    path("me/", ManageUserAPIView.as_view(), name="manage"),
    path("", include(router.urls)),
]

app_name = "user"
