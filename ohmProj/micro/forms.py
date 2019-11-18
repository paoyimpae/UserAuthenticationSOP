from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = (
            'username',
            # 'first_name',
            # 'last_name',
            'email',
            'password1',
            'password2'
        )

    def clean_username(self):
        data = self.cleaned_data['username']

        if len(data) < 5 or len(data) > 15:
            raise forms.ValidationError('Username ต้องอยู่ระหว่าง 5-15ตัวอักษร')
        return data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
