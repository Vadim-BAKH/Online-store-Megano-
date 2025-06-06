from django.forms import ModelForm, inlineformset_factory

from .._models import Specification, Product


class SpecificationForm(ModelForm):
    class Meta:
        model = Specification
        fields = ('name', 'value',)


SpecificationFormSet = inlineformset_factory(
    Product,
    Specification,
    form=SpecificationForm,
    extra=2,
    can_delete=True,
)