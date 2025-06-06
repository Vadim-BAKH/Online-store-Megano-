from django.urls import path

from ._views import ProductsListView, ProductCreateView, ProductUpdateView, ProductDeleteByIdView, ProductReturnByIdView, ProductCatalogAPIView, TagListAPIView

app_name = "shop"

urlpatterns = [
    path("products/", ProductsListView.as_view(), name="products_table"),
    path("product/create/", ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="update_product"),
    path("product/delete/", ProductDeleteByIdView.as_view(), name="delete_product"),
    path("product/return/", ProductReturnByIdView.as_view(), name="return_product"),
    path('api/catalog/', ProductCatalogAPIView.as_view(), name='api_catalog'),
    path('api/tags/', TagListAPIView.as_view(), name='api_tags'),

]
