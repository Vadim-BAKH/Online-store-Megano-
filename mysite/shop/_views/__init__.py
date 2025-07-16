"""Инициализация вью."""

__all__ = [
    "BasketAPIView",
    "BannerListAPIView",
    "ProductsListView",
    "ProductUpdateView",
    "PaymentOrderApi",
    "ProductDetailAPIView",
    "ProductCatalogAPIView",
    "PopularProductsAPIView",
    "ProductReviewCreateView",
    "ProductCreateView",
    "ProductReturnByIdView",
    "ProductDeleteByIdView",
    "LimitedProductListAPIView",
    "RandomAccountApi",
    "CategoryApiView",
    "TagListAPIView",
    "OrderDetailView",
    "CreateOrderView",
    "UserOrderListApi",
    "SalesAPIView",
]

from .banners_api import BannerListAPIView
from .basket_api import BasketAPIView
from .catalog_api import ProductCatalogAPIView
from .categories_api import CategoryApiView
from .history_orders_api import UserOrderListApi
from .limit_products_api import LimitedProductListAPIView
from .order_api import CreateOrderView
from .order_by_id_api import OrderDetailView
from .payment_api import PaymentOrderApi
from .payment_order_api import RandomAccountApi
from .product_create import ProductCreateView
from .product_detail_api import ProductDetailAPIView
from .product_popular_api import PopularProductsAPIView
from .product_return import ProductReturnByIdView
from .product_soft_delete import ProductDeleteByIdView
from .product_update import ProductUpdateView
from .products_table_view import ProductsListView
from .review_api import ProductReviewCreateView
from .sale_api import SalesAPIView
from .tag_api import TagListAPIView
