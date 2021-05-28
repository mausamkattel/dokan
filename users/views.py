from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


class EditProfileView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'avatar')
    template_name = "registration/edit_user.html"
    success_url = reverse_lazy("core:dashboard")


class LoginView(LoginView):
    authentication_form = UserLoginForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()

            messages.success(
                request, f'Your account was successfully created! You can now login!')
            return redirect(reverse("core:dashboard"))
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})
