"""
Форма администратора для модели оплаты.

Валидация полей банковской карты.
"""

import re

from django import forms
from django.core.exceptions import ValidationError

from .._models import Payment


class PaymentAdminForm(forms.ModelForm):

    """Форма для валидации полей платежной информации в админке."""

    class Meta:

        """Метаданные модели и полей."""

        model = Payment
        fields = "__all__"

    def clean_number(self):
        """Проверяет, что номер карты состоит из 16 цифр."""
        number = self.cleaned_data.get("number", "").replace(" ", "")
        if not re.fullmatch(r"\d{16}", number):
            raise ValidationError(
                "Номер карты должен содержать ровно 16 цифр."
            )
        return number

    def clean_month(self):
        """Проверяет, что месяц корректный (от 1 до 12)."""
        month = self.cleaned_data.get("month")
        try:
            month_int = int(month)
        except (TypeError, ValueError):
            raise ValidationError(
                "Месяц должен быть числом.",
            )
        if not (1 <= month_int <= 12):
            raise ValidationError(
                "Месяц должен быть от 1 до 12.",
            )
        return month_int

    def clean_year(self):
        """Проверяет, что год состоит из 4 цифр."""
        year = self.cleaned_data.get("year", "")
        if not re.fullmatch(r"\d{4}", str(year)):
            raise ValidationError(
                "Год должен состоять из 4 цифр.",
            )
        return year

    def clean_code(self):
        """Проверяет, что код безопасности состоит из 3 цифр."""
        code = self.cleaned_data.get("code", "")
        if not re.fullmatch(r"\d{3}", code):
            raise ValidationError(
                "Код безопасности должен содержать 3 цифры.",
            )
        return code
