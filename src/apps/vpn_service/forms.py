from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserSite


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']


class UserSiteForm(forms.ModelForm):
    class Meta:
        model = UserSite
        fields = ['name', 'original_url']
