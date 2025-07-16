"""Модуль абстрактной модели сессии."""

from django.db import models


class SessionKeyMixin(models.Model):

    """
    Абстрактная модель для хранения session_key.

    Используется для связи объектов с сессией пользователя.
    """

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Session Key",
        help_text="Уникальный ключ сессии для связи с корзиной/заказом",
    )

    class Meta:

        """Определяет модель как абстрактную."""

        abstract = True
