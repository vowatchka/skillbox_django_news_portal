from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    tel = forms.CharField(max_length=15, required=False, label="Телефон")
    city = forms.CharField(max_length=100, required=False, label="Город")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "tel", "city", "password1", "password2")
