"""API-представление для получения информации о текущем пользователе."""

from loguru import logger
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Profile
from ..serialization import ProfileSerializer


class UserStatusApi(APIView):

    """
    API для получения профиля текущего авторизованного пользователя.

    Доступен только аутентифицированным пользователям (IsAuthenticated).
    Возвращает сериализованные данные модели Profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Обрабатывает GET-запрос на получение профиля пользователя.

        Args:
            request (Request): Объект запроса от клиента.

        Returns:
            Response: JSON-ответ с данными профиля (HTTP 200).

        """
        profile = Profile.objects.select_related("user").get(
            user=request.user,
        )
        serializer = ProfileSerializer(
            profile,
            context={"request": request},
        )
        logger.debug(
            "User's status: '{}'",
            serializer.data,
        )
        return Response(serializer.data)
