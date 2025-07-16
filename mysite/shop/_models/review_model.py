"""Модель отзывов на товары."""

from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from .product_model import Product
from .soft_delete_model import SoftDeleteModel


class Review(SoftDeleteModel):

    """
    Отзыв на товар.

    Содержит автора, email, текст отзыва, оценку и дату создания.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        null=False,
        blank=False,
        db_index=True,
    )
    text = models.TextField(
        null=True,
        blank=True,
        validators=[
            MaxLengthValidator(250),
        ],
    )
    rate = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        """Метаданные модели."""

        ordering = ["-date"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        """Строковое представление."""
        product_title = getattr(
            self.product,
            "title",
            "Unknown product",
        )
        return (
            f"Review by {self.author} for product "
            f"# {product_title} - Rate: {self.rate}"
        )
