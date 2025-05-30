from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from myauth.forms import user_register_form


class RegisterView(FormView):
    template_name = "frontend/signUp_form.html"
    form_class = user_register_form.UserRegisterForm
    success_url = reverse_lazy("api:profile_update")

    def form_valid(self, form):

        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
