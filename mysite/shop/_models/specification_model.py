"""Модель характеристики товара."""

from django.db import models

from .product_model import Product
from .soft_delete_model import SoftDeleteModel


class Specification(SoftDeleteModel):

    """
    Характеристика товара.

    Пример: name = "Вес", value = "300г"
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=20,
    )
    value = models.CharField(
        null=True,
        blank=True,
        max_length=10,
    )

    def __str__(self) -> str:
        """Возвращает название характеристики."""
        return str(self.name) or ""
