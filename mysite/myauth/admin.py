"""Регистрация модели Profile в админке Django."""

from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Profile.

    Настраивает отображаемые поля, ссылки и поля поиска в админке.
    """

    list_display = ("user", "fullName", "email", "phone", "avatar")
    list_display_links = ("user", "email", "phone",)
    search_fields = ("fullName", "email", "phone",)
