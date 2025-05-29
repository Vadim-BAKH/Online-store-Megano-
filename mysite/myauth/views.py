from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, reverse, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
import json
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from .forms import UserRegisterForm, UserLoginForm



class RegisterView(FormView):
    template_name = "frontend/signUp_form.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("api:about_me")

    def form_valid(self, form):

        user = form.save()
        login(self.request, user)
        return super().form_valid(form)



class LoginView(FormView):
    template_name = "frontend/signIn_form.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("api:about_me")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


async def logout_view(request: HttpRequest) -> HttpResponse:
    await sync_to_async(logout)(request)
    return redirect(reverse("api:login"))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = getattr(user, 'profile', None)
        context['user'] = user
        context['profile'] = profile
        return context

