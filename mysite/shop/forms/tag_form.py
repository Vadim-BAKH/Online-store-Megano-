"""Форма для создания и редактирования тега."""

from django.forms import ModelForm

from .._models import Tag


class TagForm(ModelForm):

    """Форма для модели Tag."""

    class Meta:

        """Метаданные модели с полем."""

        model = Tag
        fields = ("name",)
