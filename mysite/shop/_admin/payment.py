"""Админ-конфигурация для управления платежами."""

from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver

from .._models import Payment
from ..forms import PaymentAdminForm


class PaymentInline(admin.StackedInline):

    """Инлайн-отображение модели оплаты на странице заказа."""

    model = Payment
    can_delete = False
    verbose_name_plural = "Оплата"
    fields = (
        "number",
        "name",
        "month",
        "year",
        "code",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    """Админ-панель для модели Payment."""

    form = PaymentAdminForm
    list_display = (
        "order",
        "number",
        "name",
        "month",
        "year",
    )
    search_fields = (
        "order__user__username",
        "number",
        "name",
    )
    autocomplete_fields = ("order",)

    @receiver(post_save, sender=Payment)
    def update_order_status(
        sender,
        instance: Payment,
        created: bool,
        **kwargs,
    ) -> None:
        """
        Обработчик сигнала post_save для модели Payment.

        Обновляет статус заказа на "paid" и удаляет корзину.

        Args:
            sender (Type): Модель-отправитель (Payment).
            instance (Payment): Экземпляр оплаты.
            created (bool): Флаг, указывает, была ли запись только что создана.
            **kwargs: Дополнительные аргументы.

        """
        if instance.order:
            order = instance.order
            order.status = "paid"
            order.save()
            cart = order.cart
            if cart:
                cart.items.all().delete()
                cart.delete()
