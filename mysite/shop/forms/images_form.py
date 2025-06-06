from django.forms import ModelForm, inlineformset_factory, ClearableFileInput, TextInput
from .._models import ProductImage, Product


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('src', 'alt',)
        widgets = {
            'srs': ClearableFileInput(attrs={'accept': 'image/*'}),
            'alt': TextInput(
                attrs={'maxlength': 50, 'placeholder': 'Добавьте описание'}
            ),
        }


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True,
)