"""
Форма администратора для модели заказа.

Автоматический пересчёт стоимости.
"""

from django import forms
from django.db import models

from .._models import Order


class OrderAdminForm(forms.ModelForm):

    """
    Форма для редактирования заказа в админке.

    Добавляет поле выбора типа оплаты.
    Автоматически пересчитывает сумму заказа.
    """

    PAYMENT_TYPE_CHOICES = (
        ("online", "Online"),
        ("someone", "Someone"),
    )

    payment_type = forms.ChoiceField(
        choices=PAYMENT_TYPE_CHOICES,
        label="Тип оплаты",
        required=True,
    )

    class Meta:

        """Метаданные модели с полями и виджетами."""

        model = Order
        fields = "__all__"
        widgets = {
            "total_cost": forms.NumberInput(
                attrs={"readonly": "readonly"},
            ),
        }

    def clean(self) -> dict:
        """
        Переопределяет метод clean.

        Автоматический подсчёт суммы заказа на основе текущей корзины.
        """
        cleaned_data = super().clean()
        cart = cleaned_data.get("cart")
        if cart:
            total = (
                cart.items.aggregate(
                    total=models.Sum(
                        models.F("product__price") * models.F("quantity")
                    )
                )["total"]
                or 0
            )
            cleaned_data["total_cost"] = total
        return cleaned_data
