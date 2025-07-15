"""Инициализация вью."""

__all__ = [
    "SignInApi",
    "SignOutApi",
    "personal_office_view",
    "ProfileApi",
    "ProfileAvatarApi",
    "ProfilePasswordApi",
    "SignUpApi",
    "UserStatusApi",
]

from .login_api import SignInApi
from .logout_api import SignOutApi
from .personal_view import personal_office_view
from .profile_api import ProfileApi
from .profile_avatar_api import ProfileAvatarApi
from .profile_password_api import ProfilePasswordApi
from .profile_status_api import UserStatusApi
from .register_api import SignUpApi
