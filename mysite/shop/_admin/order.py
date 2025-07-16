"""Админ-конфигурация для заказов и позиций заказов."""

from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from .._models import Order, OrderItem
from ..forms import OrderAdminForm


class OrderItemInline(admin.TabularInline):

    """Инлайн для отображения товаров, входящих в заказ."""

    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    fields = ("product", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    """Админка для модели Order."""

    form = OrderAdminForm
    ordering = ("-created_at",)
    search_fields = (
        "user__username",
        "full_name",
        "email",
        "phone",
        "address",
        "cart__id",
    )
    autocomplete_fields = ("cart",)
    list_display = (
        "id",
        "user",
        "full_name",
        "email",
        "phone",
        "payment_type",
        "status",
        "total_cost",
        "delivery_type",
        "created_at",
        "is_deleted",
        "cart_link",
    )
    fields = (
        "user",
        "cart",
        "full_name",
        "email",
        "phone",
        "city",
        "address",
        "payment_type",
        "status",
        "total_cost",
        "delivery_type",
        "payment_error",
        "created_at",
        "is_deleted",
    )
    readonly_fields = (
        "created_at",
        "payment_error",
        "total_cost",
    )

    def cart_link(self, obj: Order) -> str:
        """
        Возвращает HTML-ссылку на связанную корзину.

        Args:
            obj (Order): Объект заказа.

        Returns:
            str: HTML-ссылка или "-" если корзина отсутствует.

        """
        if obj.cart:
            url = f"/admin/shop/cart/{obj.cart.id}/change/"
            return format_html(
                '<a href="{}">Корзина #{}</a>', url, obj.cart.id
            )
        return "-"

    cart_link.short_description = "Корзина"

    def save_model(self, request, obj, form, change):
        if obj.cart:
            total = (
                obj.cart.items.aggregate(
                    total=models.Sum(
                        models.F("product__price") * models.F("quantity")
                    )
                )["total"]
                or 0
            )
            obj.total_cost = total
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    """Админ-панель для модели OrderItem."""

    list_display = ("order", "product", "quantity")
    list_filter = ("product",)
    search_fields = ("order__user__username", "product__title")
    autocomplete_fields = ("order", "product")
