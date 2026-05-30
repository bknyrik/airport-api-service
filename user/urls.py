from django.urls import path

from user.views import CreateUserAPIView, ManageUserAPIView


urlpatterns = [
    path("register/", CreateUserAPIView.as_view(), name="create"),
    path("me/", ManageUserAPIView.as_view(), name="manage")
]

app_name = "user"
