"""Форма и формсет для характеристик товара (Specification)."""

from django.forms import ModelForm, inlineformset_factory

from .._models import Product, Specification


class SpecificationForm(ModelForm):

    """Форма для одной характеристики товара."""

    class Meta:

        """Метаданные модели с полями."""

        model = Specification
        fields = (
            "name",
            "value",
        )


SpecificationFormSet = inlineformset_factory(
    Product,
    Specification,
    form=SpecificationForm,
    extra=2,
    can_delete=True,
)
