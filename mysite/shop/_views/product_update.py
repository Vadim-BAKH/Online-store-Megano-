

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from loguru import logger

from .._models import Product
from ..forms import ProductForm
from ..product_mixin import ProductMixin

class ProductUpdateView(ProductMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/product_manager.html"
    success_url = reverse_lazy("shop:products_table")

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        initial = self._get_category_initial(product)

        form = self.form_class(instance=product, initial=initial)
        image_formset, spec_formset = self.get_formsets(request, product)

        context = {
            "form": form,
            "image_formset": image_formset,
            "spec_formset": spec_formset,
            "product": product,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=product)
        image_formset, spec_formset = self.get_formsets(request, product)

        if form.is_valid() and image_formset.is_valid() and spec_formset.is_valid():
            cd = form.cleaned_data

            # Получаем или создаём категории через миксин
            category, subcategory = self.get_or_create_categories(cd, form)
            if not (subcategory or category):
                return self._handle_validation_error(request, form, image_formset, spec_formset, product)

            # Присваиваем категорию товару
            form.instance.category = subcategory if subcategory else category

            product = form.save()
            self.handle_tags(product, cd.get('new_tags', ''))
            self.handle_formsets(product, image_formset, spec_formset)

            logger.debug(f"Товар {product.title} обновлён.")
            messages.success(request, f"Товар {product.title} успешно обновлён")
            return redirect(self.success_url)

        return self._handle_validation_error(request, form, image_formset, spec_formset, product)

    def _get_category_initial(self, product):
        initial = {}
        if product.category:
            if product.category.parent is None:
                initial['category'] = product.category
                initial['subcategory'] = None
            else:
                initial['category'] = product.category.parent
                initial['subcategory'] = product.category
        return initial

    def _handle_validation_error(self, request, form, image_formset, spec_formset, product):
        logger.error(f"Ошибки при обновлении: {form.errors}")
        context = {
            "form": form,
            "image_formset": image_formset,
            "spec_formset": spec_formset,
            "product": product,
        }
        return render(request, self.template_name, context)

# class ProductUpdateView(UserPassesTestMixin, UpdateView):
#     model = Product
#     template_name = "shop/product_manager.html"
#     success_url = reverse_lazy("shop:products_table")
#
#     def test_func(self):
#         return self.request.user.is_staff
#
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         product = get_object_or_404(Product, pk=pk)
#
#         initial = {}
#         if product.category:
#             if product.category.parent is None:
#                 # Категория — корневая
#                 initial['category'] = product.category
#                 initial['subcategory'] = None
#             else:
#                 # Категория — подкатегория
#                 initial['category'] = product.category.parent
#                 initial['subcategory'] = product.category
#
#         form = ProductForm(instance=product, initial=initial)
#         image_formset = ProductImageFormSet(queryset=ProductImage.objects.filter(product=product))
#         spec_formset = SpecificationFormSet(queryset=Specification.objects.filter(product=product))
#
#         context = {
#             "form": form,
#             "image_formset": image_formset,
#             "spec_formset": spec_formset,
#             "product": product,
#         }
#         logger.debug(f"Товар {product.title} открыт для редактирования")
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         product = get_object_or_404(Product, pk=pk)
#
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         image_formset = ProductImageFormSet(
#             request.POST,
#             request.FILES,
#             queryset=ProductImage.objects.filter(product=product)
#         )
#         spec_formset = SpecificationFormSet(
#             request.POST,
#             queryset=Specification.objects.filter(product=product)
#         )
#
#         if form.is_valid() and image_formset.is_valid() and spec_formset.is_valid():
#             cd = form.cleaned_data
#
#             # Определяем корневую категорию
#             category = None
#             if cd.get('new_category'):
#                 category, created = Category.objects.get_or_create(
#                     title=cd['new_category'],
#                     parent=None,
#                     defaults={
#                         "src": cd.get("new_category_image"),
#                         "alt": cd.get("new_category_alt") or cd['new_category']
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
#                     context = {
#                         "form": form,
#                         "image_formset": image_formset,
#                         "spec_formset": spec_formset,
#                         "product": product,
#                     }
#                     return render(request, self.template_name, context)
#                 subcategory, created = Category.objects.get_or_create(
#                     title=cd['new_subcategory'],
#                     parent=category,
#                     defaults={
#                         "src": cd.get("new_subcategory_image"),
#                         "alt": cd.get("new_subcategory_alt") or cd['new_subcategory']
#                     }
#                 )
#             elif cd.get('subcategory'):
#                 subcategory = cd['subcategory']
#
#             # Присваиваем категорию: подкатегорию, если есть, иначе корневую
#             if subcategory:
#                 form.instance.category = subcategory
#             elif category:
#                 form.instance.category = category
#             else:
#                 form.add_error('category', 'Необходимо выбрать категорию или подкатегорию')
#                 context = {
#                     "form": form,
#                     "image_formset": image_formset,
#                     "spec_formset": spec_formset,
#                     "product": product,
#                 }
#                 return render(request, self.template_name, context)
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
#             # Сохраняем formset’ы, назначая instance
#             image_formset.instance = product
#             image_formset.save()
#
#             spec_formset.instance = product
#             spec_formset.save()
#
#             logger.debug(f"Товар {product.title} обновлён")
#             messages.success(request, f"Товар {product.title} успешно обновлён")
#             return redirect(self.success_url)
#         else:
#             # При ошибках повторно инициализируем initial
#             initial = {}
#             if product.category:
#                 if product.category.parent is None:
#                     initial['category'] = product.category
#                     initial['subcategory'] = None
#                 else:
#                     initial['category'] = product.category.parent
#                     initial['subcategory'] = product.category
#             form = ProductForm(request.POST, request.FILES, instance=product, initial=initial)
#
#             context = {
#                 "form": form,
#                 "image_formset": image_formset,
#                 "spec_formset": spec_formset,
#                 "product": product,
#             }
#             return render(request, self.template_name, context)
