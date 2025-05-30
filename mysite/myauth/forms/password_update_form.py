"""Формы для действий с профилем пользователя"""
from django import forms

from django.contrib.auth import get_user_model


from django.core.exceptions import ValidationError



User = get_user_model()





class PasswordUpdateForm(forms.Form):
    passwordCurrent = forms.CharField(
        widget=forms.PasswordInput,
        label="Текущий пароль"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Новый пароль"
    )
    passwordReply = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтверждение пароля"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_passwordCurrent(self):
        current_password = self.cleaned_data.get("passwordCurrent")
        if not self.user.check_password(current_password):
            raise ValidationError("Текущий пароль введён неверно.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        pwd_rep = cleaned_data.get("passwordReply")

        if not pwd or not pwd_rep:
            raise ValidationError("Заполните все поля для пароля.")

        if pwd != pwd_rep:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data.get('password')
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user
