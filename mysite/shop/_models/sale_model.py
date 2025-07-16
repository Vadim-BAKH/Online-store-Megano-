"""Модель скидки на продукт."""

from django.db import models
from django.utils import timezone


class Sale(models.Model):

    """Модель скидки на продукт."""

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    date_from = models.DateField(
        default=timezone.now,
    )
    date_to = models.DateField()
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:

        """Метаданные модели скидки."""

        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
        ordering = ["-date_from"]

    def __str__(self) -> str:
        """
        Строковое представление скидки.

        Returns:
            str: Текстовое описание скидки.

        """
        return f"Sale #{self.id} - {self.product.title}"
