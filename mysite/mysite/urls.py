"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from loguru import logger
from myauth.views import (
    ProfileApi,
    ProfileAvatarApi,
    ProfilePasswordApi,
    SignInApi,
    SignOutApi,
    SignUpApi,
    UserStatusApi,
)
from shop.views import (
    BannerListAPIView,
    BasketAPIView,
    CategoryApiView,
    CreateOrderView,
    LimitedProductListAPIView,
    OrderDetailView,
    PaymentOrderApi,
    PopularProductsAPIView,
    ProductCatalogAPIView,
    ProductCreateView,
    ProductDeleteByIdView,
    ProductDetailAPIView,
    ProductReturnByIdView,
    ProductReviewCreateView,
    ProductsListView,
    ProductUpdateView,
    RandomAccountApi,
    SalesAPIView,
    TagListAPIView,
    UserOrderListApi,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("frontend.urls")),
    path("my/", include("myauth.urls")),
    path("shop/", include("shop.urls")),
]


urlpatterns += [
    path(
        "api/sign-in/",
        SignInApi.as_view(),
        name="sign-in",
    ),
    path(
        "api/sign-out/",
        SignOutApi.as_view(),
        name="sign-out",
    ),
    path(
        "api/sign-up/",
        SignUpApi.as_view(),
        name="sign-up",
    ),
    path(
        "api/profile/",
        ProfileApi.as_view(),
        name="profile",
    ),
    path(
        "api/profile/avatar/",
        ProfileAvatarApi.as_view(),
        name="profile-avatar",
    ),
    path(
        "api/profile/password/",
        ProfilePasswordApi.as_view(),
        name="profile-password",
    ),
    path(
        "api/user/",
        UserStatusApi.as_view(),
        name="user-status",
    ),
    path(
        "api/catalog/",
        ProductCatalogAPIView.as_view(),
        name="api_catalog_root",
    ),
    path(
        "api/products/limited/",
        LimitedProductListAPIView.as_view(),
        name="limited-products",
    ),
    path(
        "api/tags/",
        TagListAPIView.as_view(),
        name="api_tags_root",
    ),
    path(
        "api/categories/",
        CategoryApiView.as_view(),
        name="api_categories",
    ),
    path(
        "api/product/<int:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
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
    path(
        "api/sales/",
        SalesAPIView.as_view(),
        name="sales",
    ),
    path(
        "api/orders/<int:id>/",
        OrderDetailView.as_view(),
        name="detail_order",
    ),
    path(
        "api/orders/",
        CreateOrderView.as_view(),
        name="create_order",
    ),
    path(
        "api/payment/<int:id>/",
        PaymentOrderApi.as_view(),
        name="payment-order-api",
    ),
    path(
        "api/random-account/",
        RandomAccountApi.as_view(),
        name="random-account-api",
    ),
    path(
        "api/history-order/",
        UserOrderListApi.as_view(),
        name="order_history",
    ),
    path(
        "api/banners/",
        BannerListAPIView.as_view(),
        name="banner-list",
    ),
    path(
        "api/products/popular/",
        PopularProductsAPIView.as_view(),
        name="popular-products",
    ),
    path(
        "product/create/",
        ProductCreateView.as_view(),
        name="create_product",
    ),
    path(
        "product/<int:pk>/edit/",
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
        "products/",
        ProductsListView.as_view(),
        name="products_table",
    ),
]


if settings.DEBUG:

    logger.debug(f"DEBUG: {settings.DEBUG}")
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
