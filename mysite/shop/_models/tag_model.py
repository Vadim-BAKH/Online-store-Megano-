"""Модуль модели тэга."""

from django.db import models

from .soft_delete_model import SoftDeleteModel


class Tag(SoftDeleteModel):

    """Модель тэга  с уникальным названием."""

    name = models.CharField(
        max_length=20, null=False, unique=True, db_index=True
    )

    def __str__(self) -> str:
        """Возвращает название тега."""
        return str(self.name)
