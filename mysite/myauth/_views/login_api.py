"""API-представление для входа пользователя в систему."""

from django.contrib.auth import authenticate, login
from loguru import logger
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class SignInApi(APIView):

    """
    API для авторизации пользователя.

    Доступно всем (AllowAny). Принимает логин и пароль.
    Выполняет проверку через Django `authenticate`.
    Устанавливает сессию и вызывает `login`.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Обрабатывает POST-запрос на авторизацию пользователя.

        Args:
            request (Request): Запрос с полями 'username', 'password', 'old_sessionid'.

        Returns:
            Response:
                - 200: при успешной авторизации.
                - 401: если данные неверны.

        """
        username = request.data.get("username")
        password = request.data.get("password")
        old_sessionid = request.data.get("old_sessionid")

        logger.debug(
            "🔐 Попытка авторизации: '{}', old_sessionid='{}'",
            username,
            old_sessionid,
        )

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            logger.warning("❌ Авторизация не удалась — неверные данные")
            return Response(
                {"detail": "Неверные учетные данные"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        logger.debug(
            "✅ Пользователь прошёл аутентификацию: '{}'",
            user,
        )

        request.session["old_sessionid"] = old_sessionid
        logger.debug(
            "📦 До save: session['old_sessionid'] = '{}'",
            request.session.get("old_sessionid"),
        )

        request.session.save()
        logger.debug(
            "💾 После save: session_key = '{}'",
            request.session.session_key,
        )

        login(request, user)
        logger.info(
            "✅ Авторизация успешна: '{}'",
            user,
        )

        logger.debug(
            "📤 После login: session_key = '{}'",
            request.session.session_key,
        )
        logger.debug(
            "📤 После login: session = '{}'",
            dict(request.session),
        )

        return Response(
            {"detail": "successful operation"},
            status=status.HTTP_200_OK,
        )
