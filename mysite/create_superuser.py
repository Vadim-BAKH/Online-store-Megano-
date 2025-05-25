from os import getenv
from django.contrib.auth import get_user_model


User = get_user_model()

username = getenv("DJANGO_SUPERUSER_USERNAME")  # или из переменных окружения
email = getenv("DJANGO_SUPERUSER_EMAIL")
password = getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
