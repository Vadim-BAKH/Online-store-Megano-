"""API-представление для просмотра и обновления профиля пользователя."""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Profile
from ..serialization import ProfileSerializer, ProfileUpdateSerializer


class ProfileApi(APIView):

    """
    API для работы с профилем текущего пользователя.

    - GET: получить информацию о профиле.
    - POST: частично обновить данные профиля.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Возвращает сериализованные данные профиля текущего пользователя.

        Returns:
            Response: JSON с полями профиля (HTTP 200).

        """
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Обновляет основные поля профиля (имя, почта, телефон).

        Args:
            request (Request): Запрос с частичными данными для обновления.

        Returns:
            Response:
                - 200: если профиль успешно обновлён.
                - 400: при ошибках валидации.

        """
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(ProfileSerializer(profile).data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
