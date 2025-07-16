"""
Модель элемента заказа.

Связывает заказ с конкретным товаром и количеством.
"""

from django.db import models

from .order_model import Order
from .product_model import Product


class OrderItem(models.Model):

    """
    Элемент заказа.

    Представляет конкретный товар и его количество в рамках заказа.
    """

    order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        """
        Возвращает читаемое представление объекта.

        Returns:
            str: Строка с информацией о товаре и количестве.

        """
        return f"{self.quantity} x {self.product} (Order #{self.order.id})"
