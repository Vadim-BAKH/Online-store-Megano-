"""Представление таблицы товаров для персонала."""

from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from loguru import logger

from .._models import Product


class ProductsListView(UserPassesTestMixin, ListView):

    """Список активных товаров."""

    model = Product
    template_name = "shop/products_list.html"
    context_object_name = "products"
    paginate_by = 20

    def test_func(self):
        """Проверка доступа; is_staff."""
        return self.request.user.is_staff

    def get_queryset(self) -> Any:
        """Получить только неархивированные продукты."""
        return (
            Product.all_objects.all()
            .select_related("category")
            .order_by("-date")
        )

    def get_context_data(self, **kwargs: Any) -> dict:
        """Добавить в контекст имена модели."""
        context = super().get_context_data(**kwargs)
        logger.debug("Открыт список продуктов")
        return context
