"""Админ-панель управления скидками на товары."""

from django.contrib import admin

from .._models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    """Админ-конфигурация модели скидки (Sale)."""

    list_display = (
        "id",
        "product",
        "sale_price",
        "date_from",
        "date_to",
        "is_active",
    )
    list_filter = (
        "is_active",
        "date_from",
        "date_to",
        "product",
    )
    search_fields = ("product__title",)
    date_hierarchy = "date_from"
    list_editable = (
        "is_active",
        "sale_price",
        "date_from",
        "date_to",
    )
    autocomplete_fields = ("product",)

    def has_delete_permission(
        self,
        request,
        obj=None,
    ) -> bool:
        """Проверка разрешения на удаление скидки."""
        return super().has_delete_permission(
            request=request,
            obj=obj,
        )

    def has_view_or_change_permission(
        self,
        request,
        obj=None,
    ) -> bool:
        """Проверка разрешения на просмотр или изменение скидки."""
        return super().has_view_or_change_permission(
            request=request,
            obj=obj,
        )
