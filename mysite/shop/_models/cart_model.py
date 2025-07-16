"""
Модель корзины.

Связана с пользователем (если он авторизован).
Содержит дату создания/обновления.
"""

from django.contrib.auth import get_user_model
from django.db import models

from .session_key_mixin import SessionKeyMixin

User = get_user_model()


class Cart(SessionKeyMixin, models.Model):

    """
    Корзина товаров пользователя или сессии.

    Атрибуты:
        user (User | None): Владелец корзины (может быть анонимным).
        created_at (datetime): Дата и время создания корзины.
        updated_at (datetime): Дата и время последнего обновления.
    """

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="carts",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Строковое представление корзины.

        Returns:
            str: Идентификатор корзины и имя пользователя или "Guest".

        """
        owner = self.user.username if self.user else "Guest"
        return f"Cart #{self.pk} by {owner}"
