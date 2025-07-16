"""
Админка для корзины и её товаров.

Настраивает отображение модели Cart и CartItem в интерфейсе
"""

from django.contrib import admin

from .._models import Cart, CartItem
from .image_mixin import ImagePreviewMixin


class CartItemInline(
    ImagePreviewMixin,
    admin.TabularInline,
):

    """
    Встроенное отображение товаров в корзине в админке.

    Используется внутри CartAdmin для отображения связанных CartItem
    в виде таблицы с автозаполнением и превью изображений.
    """

    model = CartItem
    extra = 0
    fields = ("product", "quantity")
    autocomplete_fields = ("product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    """
    Админка для модели корзины Cart.

    Отображает поля пользователя, даты и количество товаров.
    """

    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
        "items_count",
    )
    search_fields = ("user__username",)
    readonly_fields = (
        "session_key",
        "created_at",
        "updated_at",
    )
    inlines = [CartItemInline]

    def items_count(self, obj: Cart) -> int:
        """
        Возвращает количество товаров в корзине.

        Args:
            obj (Cart): объект корзины

        Returns:
            int: количество элементов в корзине

        """
        return obj.items.count()

    items_count.short_description = "Количество товаров"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    """Админка для модели CartItem (товар в корзине)."""

    list_display = (
        "cart",
        "product",
        "quantity",
    )
    search_fields = (
        "cart__user__username",
        "product__title",
    )
    autocomplete_fields = (
        "cart",
        "product",
    )
