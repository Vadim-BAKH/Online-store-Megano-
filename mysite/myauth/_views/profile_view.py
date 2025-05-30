from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from myauth.forms import password_update_form, avatar_update_form, profile_update_form
from myauth.models import Profile


@login_required
def profile_update_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        profile_form = profile_update_form.ProfileUpdateForm(request.POST, instance=profile)
        avatar_form = avatar_update_form.AvatarUpdateForm(request.POST, request.FILES, instance=profile)
        password_form = password_update_form.PasswordUpdateForm(user=user)  # пустая форма для пароля

        if profile_form.is_valid() and avatar_form.is_valid():
            profile_form.save()
            avatar_form.save()
            messages.success(request, "Профиль успешно обновлён.")
            return redirect('api:profile_update')
    else:
        profile_form = profile_update_form.ProfileUpdateForm(instance=profile)
        avatar_form = avatar_update_form.AvatarUpdateForm(instance=profile)
        password_form = password_update_form.PasswordUpdateForm(user=user)

    context = {
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'password_form': password_form,
        'profile': profile,
    }
    return render(request, 'frontend/profile_forms.html', context)
