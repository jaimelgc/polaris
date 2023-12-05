from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Account, Card, Client


class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        # register with default image, modify later
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AccountRegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['alias']


class AccountModificationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['alias', 'status']


class CardCreationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['alias', 'account']


class CardModificationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['alias', 'status']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['avatar']
