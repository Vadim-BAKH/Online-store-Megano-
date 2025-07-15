"""Форма отзыва для продукта."""

from django import forms

from .._models import Review


class ReviewForm(forms.ModelForm):

    """Форма для создания отзыва на продукт."""

    class Meta:

        """Метаданные модели с полями и виджетами."""

        model = Review
        fields = ("text", "rate")
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
            "rate": forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }
