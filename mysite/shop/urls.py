"""
Маршруты приложения shop.

Управление товарами, каталогом, тегами и корзиной.
"""

from django.urls import path

from ._views import (
    BasketAPIView,
    LimitedProductListAPIView,
    ProductCatalogAPIView,
    ProductCreateView,
    ProductDeleteByIdView,
    ProductDetailAPIView,
    ProductReturnByIdView,
    ProductReviewCreateView,
    ProductsListView,
    ProductUpdateView,
    TagListAPIView,
)

app_name = "shop"

urlpatterns = [
    path(
        "products/",
        ProductsListView.as_view(),
        name="products_table",
    ),
    path(
        "product/create/",
        ProductCreateView.as_view(),
        name="create_product",
    ),
    path(
        "products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="update_product",
    ),
    path(
        "product/delete/",
        ProductDeleteByIdView.as_view(),
        name="delete_product",
    ),
    path(
        "product/return/",
        ProductReturnByIdView.as_view(),
        name="return_product",
    ),
    path(
        "api/products/limited/",
        LimitedProductListAPIView.as_view(),
        name="limited-products",
    ),
    path(
        "api/catalog/",
        ProductCatalogAPIView.as_view(),
        name="api_catalog",
    ),
    path(
        "api/tags/",
        TagListAPIView.as_view(),
        name="api_tags",
    ),
    path(
        "api/product/<int:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product_detail",
    ),
    path(
        "api/product/<int:product_id>/reviews/",
        ProductReviewCreateView.as_view(),
        name="reviews",
    ),
    path(
        "api/basket/",
        BasketAPIView.as_view(),
        name="basket",
    ),
]
