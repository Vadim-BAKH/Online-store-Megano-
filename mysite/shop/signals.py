"""
Сигналы для привязки гостевого заказа к пользователю.

Привязка после авторизации.
"""

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from loguru import logger

from ._models import Order


@receiver(user_logged_in)
def attach_guest_order(sender, request, user, **kwargs):
    """
    Привязывает гостевой заказ из сессии к пользователю после входа.

    Если в сессии есть guest_order_id, и заказ без пользователя найден,
    он сохраняется с текущим пользователем. ID удаляется из сессии.
    """
    guest_order_id = request.session.pop("guest_order_id", None)
    if guest_order_id:
        try:
            order = Order.objects.get(id=guest_order_id, user=None)
            order.user = user
            order.save()
            logger.info(f"🧷 Заказ {order.id} прикреплён к {user}")
        except Order.DoesNotExist:
            logger.warning(
                f"❌ Гостевой заказ {guest_order_id} "
                f"не найден или уже с пользователем"
            )
