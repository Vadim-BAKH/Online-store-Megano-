"""
Модель оплаты.

Хранит платёжную информацию, связанную с конкретным заказом.
"""

from django.db import models

from .order_model import Order


class Payment(models.Model):

    """
    Платёж заказа.

    Содержит данные банковской карты, с которой была совершена оплата.
    """

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    number = models.CharField(max_length=16)
    name = models.CharField(max_length=100)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    code = models.CharField(max_length=4)

    def __str__(self) -> str:
        """
        Строковое представление платежа.

        Returns:
            str: Информация о платеже.

        """
        return f"Payment for Order {self.order.id} by {self.name}"
