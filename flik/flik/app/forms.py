# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms
from django.forms import extras

from django.utils.translation import ugettext_lazy as _

from flik.app.models import User

def PlaceholderField(placeholder, cls=forms.CharField, widgetattrs={}, *args, **kwargs):
    widgetattrs['placeholder'] = placeholder
    return cls(widget=forms.TextInput(attrs=widgetattrs),
            required=True, *args, **kwargs)

def PlaceholderEmailField(placeholder, widgetattrs={}, *args, **kwargs):
    return PlaceholderField(placeholder, forms.EmailField, widgetattrs, *args, **kwargs)

def PlaceholderCharField(placeholder, widgetattrs, *args, **kwargs):
    return PlaceholderField(placeholder, forms.CharField, widgetattrs, *args, **kwargs)

class PlaceholderPasswordInput(forms.PasswordInput):
    """
    Django form password input that turns off autocomplete and provides a shortcut
    for setting a placeholder.
    """
    def __init__(self, name, **kwargs):
        kwargs['placeholder'] = name
        kwargs['autocomplete'] = 'off'
        super(PlaceholderPasswordInput, self).__init__(attrs=kwargs)


class LoginForm(forms.Form):
    email = PlaceholderCharField("Email", widgetattrs={})
    password = forms.CharField(widget=PlaceholderPasswordInput('Password'))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            User.objects.get(email=email)
        except:
            raise forms.ValidationError(_("This email does not exist in our database"))
        else:
            return email.lower()

    def clean_password(self):
        password = self.cleaned_data['password']
        email = self.data['email'].lower()
        if len(password) < 6:
            raise forms.ValidationError(_("Password must be at least 6 characters"))
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError(_("Your password is invalid. "))
        except:
            raise forms.ValidationError(_("Your password is invalid. "))


class RegistrationForm(forms.Form):
    email = PlaceholderCharField("Email", widgetattrs={})
    password = forms.CharField(widget=PlaceholderPasswordInput('Password'))
    first_name = PlaceholderCharField("First Name", widgetattrs={})
    last_name = PlaceholderCharField("Last Name", widgetattrs={})
    company_name = PlaceholderCharField("Company Name", widgetattrs={})

    def clean_email(self):
        email = self.cleaned_data.get('email', "").lower()
        try:
            User.objects.get(email=email)
        except:
            return email
        else:
            raise forms.ValidationError(_("This Email is taken"))

    def clean_company_name(self):
        company = self.cleaned_data.get("company")
        try:
            Company.objects.get(name=company)
        except:
            return company
        else:
            raise forms.ValidationError(_("This Company is taken"))

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 1:
            raise forms.ValidationError("First name required")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 1:
            raise forms.ValidationError("Last name required")
        return last_name

