"""Конфигурация приложения."""

from django.apps import AppConfig


class FrontendConfig(AppConfig):

    """Конфигурация frontend."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "frontend"
    app_name = "frontend"
