from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from .models import Account, Card, Client


class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        validators=[validate_password],
    )
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError(_("Passwords don't match."))
        return cd.get('password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email already in use.'))
        elif email == '':
            raise forms.ValidationError(_('Email is required for registration.'))
        return email

    def clean_first_name(self):
        if first_name := self.cleaned_data.get('first_name'):
            return first_name
        raise forms.ValidationError(_('First name is required for registration.'))

    def clean_last_name(self):
        if last_name := self.cleaned_data.get('last_name'):
            return last_name
        raise forms.ValidationError(_('Last name is required for registration.'))


class LoginForm(forms.Form):
    username = forms.CharField(label=_('username'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)


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
