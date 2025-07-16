"""
Миксин для админки, добавляющий поддержку мягкого удаления.

Позволяет просматривать, удалять и восстанавливать объекты.
"""

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path


class SoftDeleteAdminMixin:

    """
    Миксин для Django Admin, добавляющий действия.

    - мягкое удаление (soft delete),
    - восстановление объектов (undelete),
    - фильтрацию по полю `is_deleted`.
    """

    actions = ["soft_delete_selected", "undelete_selected"]
    list_filter = ("is_deleted",)  # Фильтр по soft delete

    def get_queryset(self, request):
        """
        Возвращает QuerySet с удалёнными и не удалёнными объектами.

        Использует менеджер `all_objects`.
        """
        qs = self.model.all_objects.all()
        # Можно по умолчанию показывать только не удалённые (если нужно)
        # return qs.filter(is_deleted=False)
        return qs

    def delete_model(self, request, obj) -> None:
        """Переопределяет удаление одного объекта на мягкое удаление."""
        obj.delete()

    def delete_queryset(self, request, queryset) -> None:
        """Переопределяет массовое удаление на мягкое удаление."""
        for obj in queryset:
            obj.delete()
        self.message_user(
            request,
            f"{queryset.count()} объектов помечены как удалённые.",
            level=messages.SUCCESS,
        )

    def soft_delete_selected(self, request, queryset):
        """Мягко удалить выбранные объекты."""
        count = queryset.update(is_deleted=True)
        self.message_user(
            request,
            f"{count} объектов помечены как удалённые.",
            level=messages.SUCCESS,
        )

    soft_delete_selected.short_description = "Мягко удалить выбранные объекты"

    def undelete_selected(self, request, queryset) -> None:
        """Восстановить ранее удалённые объекты."""
        count = queryset.update(is_deleted=False)
        self.message_user(
            request, f"{count} объектов восстановлены.", level=messages.SUCCESS
        )

    undelete_selected.short_description = "Восстановить выбранные объекты"

    # Добавим кнопки для восстановления в change_view
    def get_urls(self):
        """Добавляет кастомный URL для восстановления объекта из change_view."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/undelete/",
                self.admin_site.admin_view(self.undelete_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_undelete",
            ),
        ]
        return custom_urls + urls

    def undelete_view(self, request, object_id):
        """Представление, восстанавливающее объект."""
        obj = self.get_object(request, object_id)
        if obj is None:
            self.message_user(request, "Объект не найден.", level=messages.ERROR)
            return redirect("..")
        obj.undelete()
        self.message_user(
            request, "Объект успешно восстановлен.", level=messages.SUCCESS
        )
        return redirect("..")

    # Добавим кнопку "Восстановить" в change_form
    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Добавляет переменную `show_undelete` в контекст."""
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context["show_undelete"] = obj.is_deleted if obj else False
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )
