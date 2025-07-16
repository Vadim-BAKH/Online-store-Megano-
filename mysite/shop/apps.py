"""Конфигурация приложения 'shop' и подключение сигналов."""

from django.apps import AppConfig
from loguru import logger


class ShopConfig(AppConfig):

    """Конфигуратор приложения."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"

    def ready(self):
        """
        Импортирует модуль signals при инициализации приложения.

        Необходимо для активации сигналов (например, user_logged_in).
        """
        logger.debug("📦 Загрузка signals.py")
        import shop.signals  # noqa
