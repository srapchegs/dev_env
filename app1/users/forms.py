from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User

class UserLoginForm(AuthenticationForm):
    class Meta:
        model=User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "otchestvo",
            "username",
            "email",
            "address",
            "phone",
            "password1",
            "password2",
        )
