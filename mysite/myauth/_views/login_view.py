from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from myauth.forms import user_login_form


class LoginView(FormView):
    template_name = "frontend/signIn_form.html"
    form_class = user_login_form.UserLoginForm
    success_url = reverse_lazy("api:personal_office")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
