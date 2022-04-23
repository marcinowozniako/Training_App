from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True, min_length=6, max_length=30)

    class Meta:
        model = get_user_model()
        fields = ('username',)


class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
