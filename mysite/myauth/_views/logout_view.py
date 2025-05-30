
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("api:login"))
