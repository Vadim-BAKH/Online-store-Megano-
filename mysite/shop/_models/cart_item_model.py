"""
Модель позиции в корзине.

Содержит связь между корзиной и продуктом, а также количество.
"""

from django.db import models

from .cart_model import Cart
from .product_model import Product


class CartItem(models.Model):

    """
    Позиция товара в корзине.

    Атрибуты:
        cart (Cart): Ссылка на корзину;
        product (Product): Продукт, добавленный в корзину;
        quantity (int): Количество единиц товара.
    """

    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        """
        Строковое представление позиции корзины.

        Returns:
            str: Текст вида "2 x Товар (Cart #ID)"

        """
        return f"{self.quantity} x {self.product} (Cart #{self.cart.id},)"
