from django.forms import ModelForm

from .._models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('author', 'email', 'text', 'rate',)
