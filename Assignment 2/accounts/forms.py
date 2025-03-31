from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission

from .models import Profile


class RegisterForm(UserCreationForm):
    gender = forms.Select(attrs={'required': 'required',})

    class Meta:
        model = Profile
        fields = ["username", "password1", "password2", "email", "gender"]


