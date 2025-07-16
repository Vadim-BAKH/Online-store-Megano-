"""
Модель настроек доставки.

Описывает параметры для расчёта обычной и экспресс-доставки.
Ограничена одной записью в базе.
"""

from django.db import models


class DeliverySettings(models.Model):

    """
    Настройки доставки.

    Включают порог для бесплатной доставки, стоимость обычной
    и экспресс-доставки. Поддерживается только одна запись.
    """

    free_delivery_threshold = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2000,
        verbose_name="Порог бесплатной доставки",
    )
    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=200,
        verbose_name="Стоимость доставки при сумме ниже порога",
    )
    express_delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500,
        verbose_name="Стоимость экспресс-доставки",
    )

    class Meta:
        verbose_name = "Настройка доставки"
        verbose_name_plural = "Настройки доставки"

    def __str__(self) -> str:
        """
        Возвращает читаемое представление объекта.

        Returns:
            str: Название модели.

        """
        return "Настройки доставки"

    def save(self, *args, **kwargs) -> None:
        """
        Сохраняет модель, не допуская более одной записи в БД.

        Raises:
            Exception: При попытке создать более одной записи.

        """
        if not self.pk and DeliverySettings.objects.exists():
            raise Exception(
                "Можно создать только одну запись DeliverySettings",
            )
        return super().save(*args, **kwargs)
