from django.forms import ModelForm

from .._models import Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
