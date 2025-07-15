"""API-представление для регистрации нового пользователя."""

from django.contrib.auth import login
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serialization import SignUpSerializer


class SignUpApi(APIView):

    """
    API-представление для регистрации пользователя.

    Разрешает неавторизованным пользователям отправку POST-запроса
    с данными для регистрации. В случае успешной регистрации
    автоматически авторизует пользователя.
    """

    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request: Request) -> Response:
        """
        Обрабатывает POST-запрос на регистрацию нового пользователя.

        Args:
            request (Request): Объект запроса с данными пользователя.

        Returns:
            Response:
                - 201: при успешной регистрации и авторизации.
                - 400: если данные невалидны.

        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(
                {"detail": "successful operation"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
