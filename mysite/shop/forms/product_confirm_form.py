"""Форма подтверждения действия с товаром по его ID."""

from django import forms


class ProductConfirmForm(forms.Form):

    """
    Простая форма.

    Подтверждение действия с товаром по его идентификатору.
    """

    product_id = forms.IntegerField(
        label="ID товара",
        min_value=1,
    )
