"""Генерация номера карты."""

from random import randint

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RandomAccountApi(APIView):

    """APIView для генерации случайного 16-значного номера счёта."""

    def get(self, request: Request) -> Response:
        """Возвращает JSON с генерированным номером счёта."""
        number = randint(1000_0000_0000_0000, 9999_9999_9999_9999)

        return Response(
            {"number": str(number)},
            status=status.HTTP_200_OK,
        )
