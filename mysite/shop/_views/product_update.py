"""Представление для обновления товара по ID через форму."""

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from loguru import logger

from .._models import Product
from ..forms import ProductForm
from ..product_utils.product_mixin import ProductMixin


class ProductUpdateView(
    ProductMixin,
    UserPassesTestMixin,
    UpdateView,
):

    """Представление обновления товара для персонала."""

    model = Product
    form_class = ProductForm
    template_name = "shop/product_manager.html"
    success_url = reverse_lazy("shop:products_table")

    def test_func(self) -> bool:
        """Разрешает доступ только администраторам."""
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Возвращает все товары, включая мягко удалённые.

        Используется кастомный менеджер `Product.all_objects`.
        """
        return Product.all_objects.all()

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обработка GET-запроса: отображение формы редактирования товара.

        Args:
            request: объект запроса.

        Returns:
            HTML-страница с формами.

        """
        product = self.get_object()
        initial = self._get_category_initial(product)

        form = self.form_class(instance=product, initial=initial)
        image_formset, spec_formset = self.get_formsets(
            request,
            product,
        )

        context = {
            "form": form,
            "image_formset": image_formset,
            "spec_formset": spec_formset,
            "product": product,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обработка POST-запроса: обновление товара и его формсетов.

        Args:
            request: объект запроса.

        Returns:
            Редирект при успехе или повторный рендер формы с ошибками.

        """
        product = self.get_object()
        form = self.form_class(
            request.POST,
            request.FILES,
            instance=product,
        )
        image_formset, spec_formset = self.get_formsets(
            request,
            product,
        )

        if form.is_valid() and image_formset.is_valid() and spec_formset.is_valid():
            cd = form.cleaned_data

            # Получаем или создаём категории через миксин
            category, subcategory = self.get_or_create_categories(
                cd,
                form,
            )
            if not (subcategory or category):
                return self._handle_validation_error(
                    request,
                    form,
                    image_formset,
                    spec_formset,
                    product,
                )

            # Присваиваем категорию товару
            form.instance.category = subcategory if subcategory else category

            product = form.save()
            self.handle_tags(product, cd.get("new_tags", ""))
            self.handle_formsets(product, image_formset, spec_formset)

            logger.debug(f"Товар {product.title} обновлён.")
            messages.success(request, f"Товар {product.title} успешно обновлён")
            return redirect(self.success_url)

        return self._handle_validation_error(
            request, form, image_formset, spec_formset, product
        )

    def _get_category_initial(self, product: Product) -> dict:
        """
        Возвращает значения для полей `category` и `subcategory.

        Args:
            product: текущий товар.

        Returns:
            Словарь с начальными значениями.

        """
        initial = {}
        if product.category:
            if product.category.parent is None:
                initial["category"] = product.category
                initial["subcategory"] = None
            else:
                initial["category"] = product.category.parent
                initial["subcategory"] = product.category
        return initial

    def _handle_validation_error(
        self, request, form, image_formset, spec_formset, product
    ):
        """
        Обрабатывает невалидные данные формы.

        Args:
            request: объект запроса.
            form: основная форма товара.
            image_formset: формсет изображений.
            spec_formset: формсет спецификаций.
            product: товар.

        Returns:
            HTML-страница с формой и ошибками.

        """
        logger.error(f"Ошибки при обновлении: {form.errors}")
        context = {
            "form": form,
            "image_formset": image_formset,
            "spec_formset": spec_formset,
            "product": product,
        }
        return render(request, self.template_name, context)
