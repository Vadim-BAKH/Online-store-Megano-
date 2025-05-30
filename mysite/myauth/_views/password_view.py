from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from myauth.forms import password_update_form
from myauth.models import Profile


@login_required
def update_password(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        password_form = password_update_form.PasswordUpdateForm(user=user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Пароль успешно изменён.")
            return redirect('api:profile_update')
    else:
        password_form = password_update_form.PasswordUpdateForm(user=user)

    context = {
        'password_form': password_form,
        'profile': profile,
    }
    return render(request, 'frontend/profile_forms.html', context)
