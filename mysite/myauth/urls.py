"""
URL-конфигурация приложения 'my'.

Содержит маршрут для личного кабинета пользователя.
"""

from django.urls import path

from ._views import personal_office_view

app_name = "my"


urlpatterns = [
    path(
        "profile/",
        personal_office_view,
        name="personal_office",
    ),
]
