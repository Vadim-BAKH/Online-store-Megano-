"""
Модель заказа.

Хранит информацию о заказе пользователя.
"""

from django.contrib.auth import get_user_model
from django.db import models

from .cart_model import Cart
from .delivery_fee_model import DeliverySettings
from .soft_delete_model import SoftDeleteModel

User = get_user_model()


class Order(SoftDeleteModel):

    """
    Заказ пользователя.

    Содержит информацию о пользователе, корзине.
    Информация о доставке, оплате и статусе заказа.
    """

    DELIVERY_CHOICES = (
        ("delivery", "Доставка"),
        ("express", "Экспресс-доставка"),
        ("ordinary", "Обычная доставка"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=25,
        null=False,
    )
    email = models.EmailField(null=False, db_index=True)
    phone = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        default="",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    payment_type = models.CharField(
        max_length=50,
    )
    status = models.CharField(
        max_length=50,
        default="new",
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    cart = models.ForeignKey(
        Cart,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name="Корзина",
    )
    delivery_type = models.CharField(
        max_length=50,
        choices=DELIVERY_CHOICES,
        default="delivery",
        verbose_name="Тип доставки",
    )
    payment_error = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ошибка оплаты",
    )

    def __str__(self) -> str:
        """
        Строковое представление заказа.

        Returns:
            str: Информация о заказе.

        """
        return (
            f"Order(pk={self.pk},"
            f" total_cost={self.total_cost!r},"
            f" created_at={self.created_at})"
        )

    def get_delivery_cost(self) -> float:
        """
        Возвращает стоимость с учётом порога бесплатной и экспресс-доставки.

        Returns:
            float: Итоговая стоимость доставки.

        """
        settings = DeliverySettings.objects.first()
        if settings is None:
            free_threshold = 2000
            delivery_fee = 200
            express_fee = 500
        else:
            free_threshold = settings.free_delivery_threshold
            delivery_fee = settings.delivery_fee
            express_fee = settings.express_delivery_fee

        if self.delivery_type == "express":
            # Экспресс-доставка = обычная доставка + express_fee
            base_fee = 0 if self.total_cost >= free_threshold else delivery_fee
            return base_fee + express_fee
        elif self.delivery_type == "delivery":
            return 0 if self.total_cost >= free_threshold else delivery_fee
        else:
            return 0
