"""Представление для восстановления удалённого товара по ID."""

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from loguru import logger

from .._models import Product
from ..forms import ProductConfirmForm


class ProductReturnByIdView(UserPassesTestMixin, View):

    """
    Представление для восстановления удалённого товара по его ID.

    Доступ разрешён только администраторам (is_staff).
    """

    template_name = "shop/product_return.html"

    def test_func(self) -> bool:
        """
        Проверка, имеет ли пользователь административные права.

        Returns:
            bool: True, если пользователь — staff.

        """
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Отображает форму ввода ID товара для восстановления.

        Args:
            request (HttpRequest): HTTP-запрос от клиента.

        Returns:
            HttpResponse: HTML-страница с формой.

        """
        form = ProductConfirmForm()
        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Обрабатывает ввод ID и восстанавливает соответствующий товар.

        Args:
            request (HttpRequest): HTTP-запрос с данными формы.

        Returns:
            HttpResponse: Перенаправление при успехе или повторный рендер.

        """
        form = ProductConfirmForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data["product_id"]
            try:
                product = Product.all_objects.get(pk=product_id)
            except Product.DoesNotExist:
                form.add_error(
                    "product_id",
                    "Товар с таким ID не найден.",
                )
                return render(
                    request,
                    self.template_name,
                    {"form": form},
                )
            product.undelete()
            messages.success(
                request,
                f"Товар ID #{product_id} успешно разархивирован",
            )
            logger.debug("Товар '{}' возвращён из архива", product_id)
            return redirect("shop:products_table")
        return render(
            request,
            self.template_name,
            {"form": form},
        )
