from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']    