"""Миксин для категорий и подкатегорий товара."""

from django import forms
from shop.forms import ProductImageFormSet, SpecificationFormSet
from shop.models import (
    Category,
    Product,
    ProductImage,
    Specification,
    Tag,
)


class ProductMixin:

    """Общая логика для вьюшек создания и обновления товаров."""

    def get_or_create_categories(self, cd: dict, form: forms.ModelForm):
        """Обработка категорий и подкатегорий."""
        category, subcategory = None, None

        # Корневая категория
        if cd.get("new_category"):
            category, _ = Category.all_objects.get_or_create(
                title=cd["new_category"],
                parent=None,
                defaults={
                    "src": cd.get("new_category_image"),
                    "alt": cd.get("new_category_alt") or cd["new_category"],
                },
            )
        elif cd.get("category"):
            category = cd["category"]

        # Подкатегория
        if cd.get("new_subcategory"):
            if not category:
                form.add_error(
                    "new_subcategory",
                    "Для создания подкатегории нужна корневая категория",
                )
                return None, None
            subcategory, _ = Category.all_objects.get_or_create(
                title=cd["new_subcategory"],
                parent=category,
                defaults={
                    "src": cd.get("new_subcategory_image"),
                    "alt": cd.get("new_subcategory_alt") or cd["new_subcategory"],
                },
            )
        elif cd.get("subcategory"):
            subcategory = cd["subcategory"]

        return category, subcategory

    def handle_tags(self, product: Product, new_tags_str: str):
        """Добавление новых тегов к товару."""
        if new_tags_str:
            tag_names = [tag.strip() for tag in new_tags_str.split(",") if tag.strip()]
            for name in tag_names:
                tag, _ = Tag.all_objects.get_or_create(name=name)
                product.tags.add(tag)

    def handle_formsets(
        self,
        product: Product,
        image_formset,
        spec_formset,
    ):
        """Сохранение формсетов с привязкой к товару."""
        image_formset.instance = product
        image_formset.save()

        spec_formset.instance = product
        spec_formset.save()

    def get_formsets(self, request, product=None):
        """Инициализация формсетов в зависимости от метода запроса."""
        if request.method == "POST":
            image_formset = ProductImageFormSet(
                request.POST,
                request.FILES,
                queryset=(
                    ProductImage.all_objects.filter(product=product)
                    if product
                    else ProductImage.objects.none()
                ),
            )
            spec_formset = SpecificationFormSet(
                request.POST,
                queryset=(
                    Specification.all_objects.filter(product=product)
                    if product
                    else Specification.objects.none()
                ),
            )
        else:
            image_formset = ProductImageFormSet(
                queryset=(
                    ProductImage.all_objects.filter(product=product)
                    if product
                    else ProductImage.objects.none()
                )
            )
            spec_formset = SpecificationFormSet(
                queryset=(
                    Specification.all_objects.filter(product=product)
                    if product
                    else Specification.objects.none()
                )
            )
        return image_formset, spec_formset
