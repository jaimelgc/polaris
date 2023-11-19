from django import forms
from django.contrib.auth.models import User

from .models import Account, Card, Client


class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

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

    # def clean_alias(self):
    #     cd = self.cleaned_data
    #     alias = cd['alias']
    #     user = cd['user']
    #     if Account.objects.filter(alias=alias, user=user).exists():
    #         raise forms.ValidationError('Alias already in use.')
    #     return alias


class CardCreationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['alias', 'account']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['avatar']
