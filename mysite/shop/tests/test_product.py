"""
Тесты для эндпоинтов магазина.

Каталог, детали товара, скидки, популярные товары и пр.
"""

import pytest
from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client() -> APIClient:
    """DRF-клиент для тестов."""
    return APIClient()


@pytest.fixture(autouse=True)
def load_shop_fixtures(django_db_setup, django_db_blocker):
    """Автоматически загружает фикстуры для тестов магазина."""
    with django_db_blocker.unblock():
        call_command(
            "loaddata",
            "fixtures/shop-tags-fixtures.json",
        )
        call_command(
            "loaddata",
            "fixtures/shop-categories-fixtures.json",
        )
        call_command(
            "loaddata",
            "fixtures/shop-products-fixtures.json",
        )
        call_command(
            "loaddata",
            "fixtures/shop-reviews-fixtures.json",
        )
        call_command(
            "loaddata",
            "fixtures/shop-specifications-fixtures.json",
        )


class TestProductEndpoints:

    """Набор тестов для публичных API-магазина."""

    def test_product_catalog(self, client):
        """Возвращает список товаров в каталоге."""
        url = reverse("api_catalog_root")
        response = client.get(url)
        assert response.status_code == 200
        assert "items" in response.data

    def test_product_detail(self, client):
        """Возвращает подробную информацию о товаре по ID."""
        url = reverse("product-detail", kwargs={"product_id": 1})
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == 1
        assert response.data["title"] == "Бородинский"

    def test_limited_products(self, client):
        """Возвращает товары с флагом limited_edition=True."""
        url = reverse("limited-products")
        response = client.get(url)
        assert response.status_code == 200

    def test_popular_products(self, client):
        """Возвращает популярные товары, отсортированные по покупкам."""
        url = reverse("popular-products")
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_sales(self, client):
        """Возвращает текущие акции с пагинацией."""
        url = reverse("sales")
        response = client.get(url)
        assert response.status_code == 200
        assert "items" in response.data
        assert "currentPage" in response.data
        assert "lastPage" in response.data

    def test_tags_list(self, client):
        """Проверяет, что список тегов доступен и корректно возвращается."""
        url = reverse("api_tags_root")
        response = client.get(url)
        assert response.status_code == 200
        assert "results" in response.data
        assert isinstance(response.data["results"], list)
        assert len(response.data["results"]) > 0

    def test_categories_list(self, client):
        """Проверяет, что список категорий доступен и корректно возвращается."""
        url = reverse("api_categories")
        response = client.get(url)
        assert response.status_code == 200
        assert "results" in response.data
        assert isinstance(response.data["results"], list)
        assert len(response.data["results"]) > 0

    def test_product_detail_not_found(self, client):
        """Возвращает 404, если товар с ID не найден."""
        url = reverse("product-detail", kwargs={"product_id": 999})
        response = client.get(url)
        assert response.status_code == 404
