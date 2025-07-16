"""Инициализация администратора."""

from .cart import (
    CartAdmin,
    CartItemAdmin,
    CartItemInline,
)
from .delivery import DeliverySettingsAdmin
from .image_mixin import ImagePreviewMixin
from .order import (
    OrderAdmin,
    OrderItemAdmin,
    OrderItemInline,
)
from .payment import PaymentAdmin, PaymentInline
from .product import (
    CategoryAdmin,
    ProductAdmin,
    ProductImageAdmin,
    ProductImageInline,
    ReviewAdmin,
    ReviewInline,
    Specification,
    SpecificationInline,
    SubCategoryInline,
    TagAdmin,
)
from .sale import SaleAdmin
from .soft_delete_mixin import SoftDeleteAdminMixin

__all__ = [
    "SpecificationInline",
    "Specification",
    "SubCategoryInline",
    "CategoryAdmin",
    "TagAdmin",
    "ReviewAdmin",
    "ReviewInline",
    "ProductAdmin",
    "ProductImageAdmin",
    "ProductImageInline",
    "SoftDeleteAdminMixin",
    "ImagePreviewMixin",
    "SaleAdmin",
    "DeliverySettingsAdmin",
    "CartAdmin",
    "CartItemInline",
    "CartItemAdmin",
    "OrderAdmin",
    "OrderItemAdmin",
    "OrderItemInline",
    "PaymentInline",
    "PaymentAdmin",
]
