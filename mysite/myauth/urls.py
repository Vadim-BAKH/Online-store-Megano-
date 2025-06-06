
from django.urls import path

from ._views.login_view import LoginView
from ._views.logout_view import logout_view
from ._views.password_view import update_password
from ._views.profile_view import profile_update_view
from ._views.register_view import RegisterView
from ._views.personal_view import personal_office_view

app_name = "api"



urlpatterns = [
    path("profile/", personal_office_view, name="personal_office"),
    path("profile/update/", profile_update_view, name="profile_update"),
    path("profile/password/", update_password, name="password_update"),
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
