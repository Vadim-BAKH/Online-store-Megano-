"""Админка для настроек доставки."""

from django.contrib import admin

from .._models import DeliverySettings


@admin.register(DeliverySettings)
class DeliverySettingsAdmin(admin.ModelAdmin):

    """
    Админка для модели DeliverySettings.

    Отображает порог бесплатной доставки и стоимость обычной доставки.
    """

    list_display = ("free_delivery_threshold", "delivery_fee")
