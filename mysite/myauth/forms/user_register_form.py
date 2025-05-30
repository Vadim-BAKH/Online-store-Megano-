"""Формы для действий с профилем пользователя"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


from django.core.exceptions import ValidationError

from django.forms import ModelForm



User = get_user_model()

class UserRegisterForm(ModelForm):
    name = forms.CharField(max_length=150, required=False, label="Имя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ("username",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["name"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user