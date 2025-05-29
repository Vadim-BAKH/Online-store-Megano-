"""Сериализаторы для действий с профилем пользователя"""

from django.contrib.auth import get_user_model, password_validation, authenticate
from rest_framework.validators import UniqueValidator
from adrf.serializers import ModelSerializer, Serializer
from rest_framework import serializers  # для ValidationError

User = get_user_model()

class UserRegisterSerializer(ModelSerializer):
    """Асинхронный сериализатор регистрации пользователя."""
    password = serializers.CharField(
        write_only=True,
        validators=[password_validation.validate_password],
        style={'input_type': 'password'}
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name',)

    async def create(self, validated_data):
        # create_user — синхронный, обернём в sync_to_async при вызове из вьюхи
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        return user


class UserLoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    async def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Необходимо указать имя пользователя и пароль.")

        # authenticate — синхронная, вызов оборачивайте в sync_to_async в вьюхе
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Неверное имя пользователя или пароль.")

        data['user'] = user
        return data
