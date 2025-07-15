"""
Модуль тестов авторизации и профиля пользователей.

Загружает фикстуры и проверяет вход и данные профиля.
"""

import pytest
from django.core.management import call_command
from myauth.models import Profile
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client() -> APIClient:
    """Возвращает тестовый клиент DRF."""
    return APIClient()


@pytest.fixture(autouse=True)
def load_fixtures(
    django_db_setup,
    django_db_blocker,
):
    """Загружает фикстуры пользователей и профилей."""
    with django_db_blocker.unblock():

        call_command(
            "loaddata",
            "fixtures/auth-users-fixtures.json",
        )
        call_command(
            "loaddata",
            "fixtures/myauth-profiles-fixtures.json",
        )


def test_sign_in_success(client: APIClient):
    """Проверяет успешную авторизацию пользователя 'owl'."""
    response = client.post(
        "/api/sign-in/",
        {
            "username": "owl",
            "password": "12345678",
        },
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "successful operation"


def test_profile_loaded():
    """Проверяет корректную загрузку профиля пользователя с pk=4."""
    profile = Profile.objects.get(pk=4)
    assert profile.fullName == "Сова"
    assert profile.email == "ol@mail.ru"
    assert profile.phone == "89773395045"
    assert profile.avatar.name.endswith("avatar/Сова.jpg")
    assert not profile.is_deleted
    assert profile.user.id == 2
