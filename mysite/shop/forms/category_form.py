from django.forms import ModelForm
from .._models import Category

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'parent', 'src', 'alt',)
