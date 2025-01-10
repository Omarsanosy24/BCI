from django.urls import path
from .views import *

app_name = "auth"
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path("profile/", UserInfoView.as_view(), name="profile"),


]
