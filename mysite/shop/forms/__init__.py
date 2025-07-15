"""Инициализация форм."""

__all__ = [
    "ProductForm",
    "ProductImageFormSet",
    "ProductImageForm",
    "ProductAdminForm",
    "PaymentAdminForm",
    "ProductConfirmForm",
    "SpecificationFormSet",
    "SpecificationForm",
    "OrderAdminForm",
    "TagForm",
    "ReviewForm",
]

from .category_form import ProductAdminForm
from .images_form import ProductImageForm, ProductImageFormSet
from .order_form import OrderAdminForm
from .payment_form import PaymentAdminForm
from .product_confirm_form import ProductConfirmForm
from .product_form import ProductForm
from .review_form import ReviewForm
from .specification_form import SpecificationForm, SpecificationFormSet
from .tag_form import TagForm
