from adrf.routers import DefaultRouter
from django.urls import path, include

from .views import ProfileView, logout_view, LoginView, RegisterView

app_name = "api"



urlpatterns = [
    path(
        "profile/", ProfileView.as_view(), name="about_me"
    ),
    path(
        "sign-out/", logout_view, name="logout"
    ),
    path(
        "sign-up/", RegisterView.as_view(), name="register"
    ),
    path(
        "sign-in/", LoginView.as_view(), name="login"
    )
]
