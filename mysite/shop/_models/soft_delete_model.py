"""Модуль модели с мягким удалением (soft delete)."""

from django.db import models


class SoftDeletedManager(models.Manager):

    """Менеджер, исключающий удалённые записи из выборки по умолчанию."""

    def get_queryset(self):
        """Возвращает QuerySet только с не удалёнными объектами."""
        return (
            super()
            .get_queryset()
            .filter(
                is_deleted=False,
            )
        )


class SoftDeleteModel(models.Model):

    """
    Абстрактная модель с поддержкой мягкого удаления.

    Поле `is_deleted` используется для логического удаления,
    без физического удаления записи из базы данных.
    """

    is_deleted = models.BooleanField(
        default=False,
    )

    objects = SoftDeletedManager()
    all_objects = models.Manager()

    class Meta:

        """Объявляет модель абстрактной."""

        abstract = True

    def delete(
        self,
        using: str | None = None,
        keep_parents: bool = False,
    ) -> None:
        """Логически удаляет объект, выставляя is_deleted=True."""
        self.is_deleted = True
        self.save()

    def undelete(self):
        """Восстанавливает ранее удалённый объект (is_deleted=False)."""
        self.is_deleted = False
        self.save()
