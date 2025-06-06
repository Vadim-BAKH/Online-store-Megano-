from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from loguru import logger

from ..product_mixin import ProductMixin
from .._models import Product
from ..forms import ProductForm


class ProductCreateView(ProductMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/product_manager.html"
    success_url = reverse_lazy("shop:products_table")

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_formset'], context['spec_formset'] = self.get_formsets(self.request)
        context['product'] = None
        return context

    def form_valid(self, form):
        image_formset, spec_formset = self.get_formsets(self.request)

        if image_formset.is_valid() and spec_formset.is_valid():
            product = form.save(commit=False)
            cd = form.cleaned_data

            # Обработка категорий
            category, subcategory = self.get_or_create_categories(cd, form)
            if category is None and subcategory is None and form.errors:
                return self.form_invalid(form)

            product.category = subcategory if subcategory else category
            product.save()

            # Дополнительные обработки
            self.handle_tags(product, cd.get('new_tags', ''))
            self.handle_formsets(product, image_formset, spec_formset)

            logger.debug(f"Товар {product.title} создан.")
            messages.success(self.request, f"Товар {product.title} успешно создан")
            return redirect(self.success_url)

        return self.form_invalid(form)

    def form_invalid(self, form):
        logger.error(f"Ошибки формы: {form.errors}")
        return super().form_invalid(form)

# class ProductCreateView(UserPassesTestMixin, CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = "shop/product_manager.html"
#     success_url = reverse_lazy("shop:products_table")
#
#     def test_func(self):
#         return self.request.user.is_staff
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.method == "POST":
#             context['image_formset'] = ProductImageFormSet(
#                 self.request.POST,
#                 self.request.FILES,
#                 queryset=ProductImage.objects.none()
#             )
#             context['spec_formset'] = SpecificationFormSet(
#                 self.request.POST,
#                 queryset=Specification.objects.none()
#             )
#         else:
#             context['image_formset'] = ProductImageFormSet(
#                 queryset=ProductImage.objects.none()
#             )
#             context['spec_formset'] = SpecificationFormSet(
#                 queryset=Specification.objects.none()
#             )
#         context['product'] = None
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         image_formset = context['image_formset']
#         spec_formset = context['spec_formset']
#
#         if image_formset.is_valid() and spec_formset.is_valid():
#             cd = form.cleaned_data
#
#             # Определяем корневую категорию
#             category = None
#             if cd.get('new_category'):
#                 category, created = Category.objects.get_or_create(
#                     title=cd['new_category'],
#                     parent=None,
#                     defaults={
#                         "src": form.cleaned_data.get("new_category_image"),
#                         "alt": form.cleaned_data.get("new_category_alt") or cd['new_category']
#                     }
#                 )
#             elif cd.get('category'):
#                 category = cd['category']
#
#             # Определяем подкатегорию
#             subcategory = None
#             if cd.get('new_subcategory'):
#                 if not category:
#                     form.add_error('new_subcategory', 'Для создания подкатегории нужна корневая категория')
#                     return self.form_invalid(form)
#                 subcategory, created = Category.objects.get_or_create(
#                     title=cd['new_subcategory'],
#                     parent=category,
#                     defaults={
#                         "src": form.cleaned_data.get("new_subcategory_image"),
#                         "alt": form.cleaned_data.get("new_subcategory_alt") or cd['new_subcategory']
#                     }
#                 )
#             elif cd.get('subcategory'):
#                 subcategory = cd['subcategory']
#
#             # Присваиваем продукту категорию (подкатегорию, если есть, иначе корневую)
#             form.instance.category = subcategory if subcategory else category
#
#             product = form.save()
#
#             # Обработка новых тегов
#             new_tags_str = cd.get('new_tags', '')
#             if new_tags_str:
#                 tag_names = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
#                 for name in tag_names:
#                     tag, created = Tag.objects.get_or_create(name=name)
#                     product.tags.add(tag)
#
#             # Сохраняем изображения
#             images = image_formset.save(commit=False)
#             for image in images:
#                 image.product = product
#                 image.save()
#             for image in image_formset.deleted_objects:
#                 image.delete()
#
#             # Сохраняем спецификации
#             specs = spec_formset.save(commit=False)
#             for spec in specs:
#                 spec.product = product
#                 spec.save()
#             for spec in spec_formset.deleted_objects:
#                 spec.delete()
#
#             messages.success(self.request, f"Вы успешно создали товар {product.title}")
#             return redirect(self.success_url)
#         else:
#             logger.error(f"Form errors: {form.errors}")
#             logger.error(f"Image formset errors: {image_formset.errors}")
#             logger.error(f"Spec formset errors: {spec_formset.errors}")
#             return self.render_to_response(self.get_context_data(form=form))
