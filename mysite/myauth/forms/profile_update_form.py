"""Формы для действий с профилем пользователя"""

from django.contrib.auth import get_user_model


from django.core.exceptions import ValidationError

from django.forms import ModelForm

from ..models import Profile

User = get_user_model()



class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ("fullName", "email", "phone",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Profile.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Этот email уже используется.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and Profile.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise ValidationError("Этот телефонный номер уже используется.")
        return phone
