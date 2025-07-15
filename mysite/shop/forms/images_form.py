"""Формы для загрузки изображений товаров и формсет для админки."""

from django.forms import (
    ClearableFileInput,
    ModelForm,
    TextInput,
    inlineformset_factory,
)

from .._models import Product, ProductImage


class ProductImageForm(ModelForm):

    """Форма для редактирования одного изображения товара."""

    class Meta:

        """Метаданные модели, полей и виджетов."""

        model = ProductImage
        fields = (
            "src",
            "alt",
        )
        widgets = {
            "srs": ClearableFileInput(attrs={"accept": "image/*"}),
            "alt": TextInput(
                attrs={
                    "maxlength": 50,
                    "placeholder": "Добавьте описание",
                }
            ),
        }


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True,
)
