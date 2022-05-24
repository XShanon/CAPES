from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    gapps_key = forms.PasswordInput()

    class Meta:
        model = Profile
        fields = ["username", "email", "password1", "password2", "gapps_key"]
        help_texts = {
            "gapps_key": "An Application password for Google Account. Link -> https://www.lifewire.com/get-a-password-to-access-gmail-by-pop-imap-2-1171882",
        }
