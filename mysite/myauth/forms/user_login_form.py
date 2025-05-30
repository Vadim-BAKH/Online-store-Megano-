"""Формы для действий с профилем пользователя"""

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model



User = get_user_model()

class UserLoginForm(AuthenticationForm):
    """Форма аутентификации."""