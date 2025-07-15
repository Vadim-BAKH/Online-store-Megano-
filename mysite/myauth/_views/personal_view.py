"""Представление личного кабинета пользователя."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from myauth.models import Profile
from shop.models import Order


@login_required
def personal_office_view(request) -> HttpRequest:
    """Возвращает шаблон личного кабинета."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    # # Получаем последний заказ пользователя (если есть)
    last_order = Order.objects.filter(user=user).order_by("-created_at").first()

    context = {
        "profile": profile,
        "last_order": last_order,
    }
    return render(
        request,
        "myauth/dashboard.html",
        context,
    )
