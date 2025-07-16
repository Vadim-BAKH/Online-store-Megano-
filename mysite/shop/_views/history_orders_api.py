"""API-представление для получения заказов текущего пользователя."""

from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Order, OrderItem
from ..serialization import OrderDetailSerializer


class UserOrderListApi(APIView):

    """Представление списка заказов."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        orders = (
            Order.objects.filter(user=request.user)
            .prefetch_related(
                Prefetch(
                    "order_items",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-created_at")
        )

        serializer = OrderDetailSerializer(
            orders, many=True, context={"request": request}
        )
        return Response(serializer.data)
