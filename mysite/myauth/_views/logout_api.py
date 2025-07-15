"""API-представление для выхода пользователя из системы."""

from django.contrib.auth import logout
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class SignOutApi(APIView):

    """
    API для выхода текущего пользователя (logout).

    Удаляет сессионные данные и завершает текущую авторизацию.
    """

    def post(self, request: Request) -> Response:
        logout(request)
        return Response(
            {"detail": "successful operation"},
            status=status.HTTP_200_OK,
        )
