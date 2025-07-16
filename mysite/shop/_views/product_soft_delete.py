"""Представление для архивирования товара по его ID."""

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from loguru import logger

from .._models import Product
from ..forms import ProductConfirmForm


class ProductDeleteByIdView(UserPassesTestMixin, View):

    """
    Представление для удаления (архивирования) товара по его ID.

    Доступ разрешён только администраторам (is_staff).
    """

    template_name = "shop/product_confirm_delete.html"

    def test_func(self) -> bool:
        """
        Проверяет, является ли пользователь сотрудником.

        Returns:
            bool: True, если пользователь — staff.

        """
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Отображает форму ввода ID товара для удаления.

        Args:
            request (HttpRequest): HTTP GET-запрос.

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
        Обрабатывает ввод ID и выполняет мягкое удаление товара.

        Args:
            request (HttpRequest): HTTP POST-запрос с ID товара.

        Returns:
            HttpResponse: Перенаправление при успехе или повторный рендер.

        """
        form = ProductConfirmForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data["product_id"]
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                form.add_error(
                    "product_id",
                    "Товар с таким ID не найден, или уже архивирован.",
                )
                return render(
                    request,
                    self.template_name,
                    {"form": form},
                )

            product.delete()
            messages.success(
                request,
                f"Товар ID #{product_id} успешно архивирован",
            )
            logger.debug("Товар '{}' удален а архив", product_id)
            return redirect("shop:products_table")
        return render(
            request,
            self.template_name,
            {"form": form},
        )
