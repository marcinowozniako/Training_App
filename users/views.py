from django.apps import apps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse

from training.apps import TrainingConfig
from . import forms


def registration_view(request):
    """
    Registration View for new user.
    If form is valid new user is added to group with all permissions required to
    use the rest of views on the site, if group not exists, it will be created.
    """
    form = forms.RegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            group_app, created = Group.objects.get_or_create(name=TrainingConfig.name)

            models = apps.all_models[TrainingConfig.name]
            for model in models:
                content_type = ContentType.objects.get(
                    app_label=TrainingConfig.name,
                    model=model
                )
                permissions = Permission.objects.filter(content_type=content_type)
                user.groups.add(group_app)
                group_app.permissions.add(*permissions)
            messages.success(request, 'Register Successfully!')
            return redirect(reverse('users:login'))
    return render(request, 'users/registration.html', {'form': form})


def login_view(request):
    """
    View for login of new user, if form is valid user will be log in to site, if not
    there will be messages on the site which will tell what is wrong.
    """
    if request.method == 'POST':
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user.is_active:
                login(request, user)
                messages.success(request, 'Login Successfully!')
                return redirect(reverse('home:home'))
    else:
        form = forms.LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    """
    Simple view for logout of user.
    """
    logout(request)
    messages.success(request, 'Logout Successfully! ')
    return redirect(reverse('home:home'))
