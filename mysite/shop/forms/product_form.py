"""
Форма для создания и редактирования товара.

Добавление новых категорий, подкатегорий и тегов.
"""

from django.forms import (
    BooleanField,
    CharField,
    ImageField,
    ModelChoiceField,
    ModelForm,
    ModelMultipleChoiceField,
    SelectMultiple,
    Textarea,
    TextInput,
    ValidationError,
)

from .._models import Category, Product, Tag


class ProductForm(ModelForm):

    """
    Форма для пользовательского интерфейса.

    Позволяет:
    - выбрать существующие категории и теги,
    - добавить новые категории, подкатегории и теги,
    - загрузить изображения для новых категорий.
    """

    category = ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True),
        required=False,
        empty_label="Выберите категорию",
    )
    new_category = CharField(
        max_length=50,
        required=False,
        widget=TextInput(attrs={"placeholder": "Впишите категорию"}),
        help_text="Если заполнено, будет создана новая категория.",
    )
    new_category_image = ImageField(
        required=False,
        label="Изображение новой категории",
        help_text="Загрузите изображение для новой категории",
    )
    new_category_alt = CharField(
        max_length=50,
        required=False,
        label="Описание изображения категории",
        widget=TextInput(attrs={"placeholder": "Описание изображения"}),
    )
    subcategory = ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=False),
        required=False,
        empty_label="Выберите подкатегорию",
        help_text="Если выбрана категория, можно выбрать подкатегорию.",
    )
    new_subcategory = CharField(
        max_length=50,
        required=False,
        widget=TextInput(
            attrs={"placeholder": "Впишите новую подкатегорию"},
        ),
        help_text="Если заполнено, будет создана новая подкатегория.",
    )
    new_subcategory_image = ImageField(
        required=False,
        label="Изображение новой подкатегории",
        help_text="Загрузите изображение для новой подкатегории",
    )
    new_subcategory_alt = CharField(
        max_length=50,
        required=False,
        label="Описание изображения подкатегории",
        widget=TextInput(attrs={"placeholder": "Описание изображения"}),
    )
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=SelectMultiple(
            attrs={"size": "10", "class": "form-control"},
        ),
    )
    new_tags = CharField(
        max_length=200,
        required=False,
        widget=TextInput(
            attrs={"placeholder": "Впишите тэги через запятую"},
        ),
        help_text="Если тэг существует, он будет"
        " использован, иначе создан новый.",
    )
    limited_edition = BooleanField(
        required=False,
        label="Ограниченный тираж",
        help_text="Отметьте, если товар " "относится к ограниченному тиражу",
    )

    class Meta:

        """Метаданные модели с полями и виджнтами."""

        model = Product
        fields = (
            "category",
            "subcategory",
            "price",
            "count",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "tags",
            "limited_edition",
        )
        widgets = {
            "description": Textarea(attrs={"rows": 3}),
            "fullDescription": Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        """Использовать в случае переопределения поведения и свойств."""
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Валидация полей формы.

        Проверка на дублирующие названия категорий/подкатегорий.
        Запрет на одновременный выбор и ввод новой категории/подкатегории.
        Проверка на дубликаты новых тегов.
        """
        cleaned_data = super().clean()

        # Валидация категорий
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")
        new_category = cleaned_data.get("new_category", "").strip()
        new_subcategory = cleaned_data.get("new_subcategory", "").strip()

        if (
            new_category
            and Category.objects.filter(
                title__iexact=new_category,
            ).exists()
        ):
            raise ValidationError(
                "Категория с таким названием уже существует."
            )
        if (
            new_subcategory
            and Category.objects.filter(
                title__iexact=new_subcategory,
            ).exists()
        ):
            raise ValidationError(
                "Подкатегория с таким названием уже существует."
            )
        if category and new_category:
            raise ValidationError(
                "Выберите категорию или введите новую, "
                "но не оба варианта одновременно."
            )
        if new_subcategory and subcategory:
            raise ValidationError(
                "Выберите подкатегорию или введите новую, "
                "но не оба варианта одновременно."
            )
        if not category and not new_category:
            raise ValidationError(
                "Выберите категорию или введите новую категорию."
            )

        # Валидация новых тегов — проверяем, что они не дублируют существующие
        new_tags_str = cleaned_data.get("new_tags", "").strip()
        if new_tags_str:
            new_tag_names = [
                tag.strip() for tag in new_tags_str.split(",") if tag.strip()
            ]
            existing_tag_names = set(
                Tag.objects.filter(name__in=new_tag_names).values_list(
                    "name", flat=True
                )
            )
            duplicates = existing_tag_names.intersection(new_tag_names)
            if duplicates:
                raise ValidationError(
                    f"Теги {', '.join(duplicates)} уже существуют. "
                    f"Пожалуйста, выберите их из списка."
                )

        return cleaned_data
