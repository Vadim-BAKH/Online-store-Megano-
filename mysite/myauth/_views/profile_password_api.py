"""API-представление для смены пароля пользователя."""

from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfilePasswordApi(APIView):

    """
    API для смены пароля текущего пользователя.

    Доступно только авторизованным пользователям.
    Проверяет текущий пароль и обновляет на новый, сохраняя сессию.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Обрабатывает POST-запрос на смену пароля.

        Args:
            request (Request): С полями 'currentPassword' и 'newPassword'.

        Returns:
            Response: JSON с результатом операции:
                - 400: если текущий пароль неверен.
                - 200: если смена пароля прошла успешно.

        """
        user = request.user
        current_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")

        if not user.check_password(current_password):
            return Response(
                {"detail": "Неверный текущий пароль"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response(
            {"detail": "successful operation"},
            status.HTTP_200_OK,
        )
