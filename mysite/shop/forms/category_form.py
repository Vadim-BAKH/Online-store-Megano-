"""
Форма для админки товаров с выбором категории или подкатегории.

Добавляет отступы для подкатегорий при отображении в выпадающем списке.
"""

from django import forms

from .._models import Category, Product


class ProductAdminForm(forms.ModelForm):

    """
    Форма для админки модели Product.

    Визуальное отображение иерархии категорий.
    """

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Категория или подкатегория",
        help_text="Выберите конечную категорию для товара",
    )

    class Meta:

        """Метаданные товара с полями."""

        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """Переопределяет отображение категорий с отступами для подкатегорий."""
        super().__init__(*args, **kwargs)

        choices = []
        for cat in Category.objects.select_related("parent"):
            prefix = "↳ " if cat.parent else ""
            choices.append((cat.id, f"{prefix}{cat.title}"))
        self.fields["category"].choices = choices
