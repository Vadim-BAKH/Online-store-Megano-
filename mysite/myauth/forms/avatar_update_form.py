"""Формы для действий с профилем пользователя"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


from django.core.exceptions import ValidationError

from django.forms import ModelForm

from ..models import Profile

User = get_user_model()




class AvatarUpdateForm(ModelForm):
    """Форма для обновления аватара пользователя."""

    class Meta:
        model = Profile
        fields = ("avatar",)

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 2 Мб.")
            if not avatar.content_type.startswith('image/'):
                raise ValidationError("Загрузите корректное изображение.")
        return avatar
