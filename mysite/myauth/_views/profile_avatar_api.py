"""API-представление для обновления аватара пользователя."""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Profile
from ..serialization import AvatarSerializer


class ProfileAvatarApi(APIView):

    """
    API для обновления аватара текущего пользователя.

    Доступно только авторизованным пользователям.
    Принимает файл изображения и сохраняет его в профиль.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Обрабатывает POST-запрос на обновление аватара.

        Args:
            request (Request): Запрос с файлом изображения в теле.

        Returns:
            Response:
                - 200: если аватар успешно обновлён.
                - 400: если произошла ошибка валидации.

        """
        profile = Profile.objects.get(user=request.user)
        serializer = AvatarSerializer(
            profile,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "successful operation"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "unsuccessful operation"},
            status=status.HTTP_400_BAD_REQUEST,
        )
