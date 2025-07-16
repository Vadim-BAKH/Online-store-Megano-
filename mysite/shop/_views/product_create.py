"""
Представление для создания товара.

Отражается только в кабинете персонала.
"""

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from loguru import logger

from .._models import Product
from ..forms import ProductForm
from ..product_utils.product_mixin import ProductMixin


class ProductCreateView(
    ProductMixin,
    UserPassesTestMixin,
    CreateView,
):

    """
    Админ-представление для создания нового товара.

    Только для staff-пользователей.
    """

    model = Product
    form_class = ProductForm
    template_name = "shop/product_manager.html"
    success_url = reverse_lazy("shop:products_table")

    def test_func(self) -> bool:
        """Ограничение доступа: только для сотрудников."""
        return self.request.user.is_staff

    def get_context_data(self, **kwargs) -> dict:
        """Добавляет formset'ы и объект продукта в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context["image_formset"], context["spec_formset"] = self.get_formsets(
            self.request
        )
        context["product"] = None
        return context

    def form_valid(self, form: ProductForm) -> HttpResponse:
        """
        Обработка успешной отправки формы.

        Сохраняет товар, обрабатывает категории, теги и связанные данные.
        """
        image_formset, spec_formset = self.get_formsets(self.request)

        if image_formset.is_valid() and spec_formset.is_valid():
            product = form.save(commit=False)
            cd = form.cleaned_data

            # Обработка категорий
            category, subcategory = self.get_or_create_categories(cd, form)
            if category is None and subcategory is None and form.errors:
                return self.form_invalid(form)

            product.category = subcategory if subcategory else category
            product.save()

            # Дополнительные обработки
            self.handle_tags(product, cd.get("new_tags", ""))
            self.handle_formsets(product, image_formset, spec_formset)

            logger.debug(f"Товар {product.title} создан.")
            messages.success(
                self.request,
                f"Товар {product.title} успешно создан",
            )
            return redirect(self.success_url)

        return self.form_invalid(form)

    def form_invalid(self, form: ProductForm) -> HttpResponse:
        """Логирует ошибки формы и отображает их пользователю."""
        logger.error(f"Ошибки формы: {form.errors}")
        return super().form_invalid(form)
