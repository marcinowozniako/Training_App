from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)


class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
