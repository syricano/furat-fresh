from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "postcode",
            "town_or_city",
            "county",
            "street_address1",
            "street_address2",
            "country",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "postcode": forms.TextInput(attrs={"class": "form-control"}),
            "town_or_city": forms.TextInput(attrs={"class": "form-control"}),
            "county": forms.TextInput(attrs={"class": "form-control"}),
            "street_address1": forms.TextInput(attrs={"class": "form-control"}),
            "street_address2": forms.TextInput(attrs={"class": "form-control"}),
            "country": CountrySelectWidget(attrs={"class": "form-select"}),
        }
