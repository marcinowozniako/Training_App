from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    """Registration form with custom min and max length of username"""

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True, min_length=6, max_length=30,
                                                  help_text="Required. Min 6 characters Max 30. Letters, digits and "
                                                            "@/./+/-/_ only.")

    class Meta:
        model = get_user_model()
        fields = ('username',)


class LoginForm(AuthenticationForm):
    """Login form with username and password fields"""
    class Meta:
        fields = ('username', 'password')
