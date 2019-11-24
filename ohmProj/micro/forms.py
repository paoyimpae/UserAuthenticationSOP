from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import TextInput
from .models import User



class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    telephone = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'telephone', 'password1', 'password2']