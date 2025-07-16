"""Админ-конфигурация для управления каталогом."""

from django.contrib import admin

from .._models import (
    Category,
    Product,
    ProductImage,
    Review,
    Specification,
    Tag,
)
from ..forms import ProductAdminForm
from .image_mixin import ImagePreviewMixin
from .soft_delete_mixin import SoftDeleteAdminMixin


class ProductImageInline(ImagePreviewMixin, admin.TabularInline):

    """Инлайн изображений товара в карточке продукта."""

    model = ProductImage
    extra = 1


class ReviewInline(admin.TabularInline):

    """Инлайн отзывов на товар в карточке продукта."""

    model = Review
    extra = 0
    readonly_fields = ("date",)


class SpecificationInline(admin.TabularInline):

    """Инлайн характеристик товара."""

    model = Specification
    extra = 1
    fields = ("name", "value")


class SubCategoryInline(ImagePreviewMixin, admin.TabularInline):

    """Инлайн подкатегорий внутри родительской категории."""

    model = Category
    fk_name = "parent"  # связь по полю parent
    extra = 1
    fields = (
        "title",
        "src",
        "alt",
        "image_preview",
        "is_deleted",
    )
    readonly_fields = ("image_preview",)
    show_change_link = True  # ссылка на редактирование подкатегории


@admin.register(Category)
class CategoryAdmin(
    SoftDeleteAdminMixin,
    ImagePreviewMixin,
    admin.ModelAdmin,
):

    """Админ-панель категорий."""

    list_display = (
        "title",
        "parent",
        "image_preview",
        "is_deleted",
    )
    list_filter = (
        "parent",
        "is_deleted",
    )
    search_fields = ("title",)
    readonly_fields = ("image_preview",)
    fields = (
        "title",
        "parent",
        "src",
        "alt",
        "image_preview",
        "is_deleted",
    )
    inlines = [SubCategoryInline]


@admin.register(Product)
class ProductAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):

    """Админ-панель товаров."""

    form = ProductAdminForm  #
    list_display = (
        "title",
        "price",
        "count",
        "category",
        "freeDelivery",
        "limited_edition",
        "sort_index",
        "is_deleted",
    )
    list_filter = (
        "category",
        "freeDelivery",
        "limited_edition",
        "tags",
        "is_deleted",
    )

    def display_category_hierarchy(self, obj: Product) -> str:
        """Показывает иерархию категории: родитель → подкатегория."""
        if obj.category.parent:
            return f"{obj.category.parent.title} → {obj.category.title}"
        return obj.category.title

    display_category_hierarchy.short_description = "Категория"
    search_fields = (
        "title",
        "description",
        "fullDescription",
    )
    list_editable = ("sort_index",)
    filter_horizontal = ("tags",)
    inlines = [
        ProductImageInline,
        ReviewInline,
        SpecificationInline,
    ]


@admin.register(ProductImage)
class ProductImageAdmin(
    SoftDeleteAdminMixin,
    ImagePreviewMixin,
    admin.ModelAdmin,
):

    """Админ-панель изображений товаров."""

    list_display = (
        "product",
        "alt",
        "image_preview",
        "is_deleted",
    )
    list_filter = ("product", "is_deleted")
    search_fields = ("alt", "product__title")


@admin.register(Review)
class ReviewAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):

    """Админ-панель отзывов."""

    list_display = (
        "product",
        "author",
        "email",
        "rate",
        "date",
        "is_deleted",
    )
    list_filter = (
        "product",
        "rate",
        "date",
        "is_deleted",
    )
    search_fields = (
        "author",
        "email",
        "text",
    )
    date_hierarchy = "date"


@admin.register(Tag)
class TagAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):

    """Админ-панель тегов."""

    list_display = ("name", "is_deleted")
    search_fields = ("name",)
