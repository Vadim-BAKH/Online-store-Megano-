"""API для отображения активных акций с поддержкой пагинации."""

from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Sale
from ..serialization import SaleSerializer


class SalesPagination(PageNumberPagination):

    """
    Кастомный пагинатор для вывода акций.

    Параметры:
        - page_size: количество элементов на странице.
        - page_query_param: имя параметра в URL для номера страницы.
    """

    page_size = 5
    page_query_param = "currentPage"

    def get_paginated_response(self, data):
        """
        Формирует структуру ответа с постраничными данными.

        Args:
            data: Список сериализованных объектов.

        Returns:
            Response: объект ответа с полями items, currentPage и lastPage.

        """
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )


class SalesAPIView(APIView):

    """
    Представление для получения активных скидок.

    Выводит только те скидки, у которых текущая дата входит в интервал
    между `date_from` и `date_to`.
    """

    pagination_class = SalesPagination

    def get(self, request: Request) -> Response:
        """
        Обрабатывает GET-запрос и возвращает список скидок с пагинацией.

        Args:
            request (Request): Объект запроса.

        Returns:
            Response: Пагинированный список активных скидок.

        """
        now = timezone.now().date()
        queryset = (
            Sale.objects.filter(date_from__lte=now, date_to__gte=now)
            .select_related("product")
            .prefetch_related("product__images")
        )

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = SaleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
