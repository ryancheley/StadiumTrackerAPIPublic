from django import forms
from django.contrib.auth.forms import UserChangeForm
from django_registration.forms import RegistrationForm
from .models import CustomUser

# Note: Must keep email in order to be able to use the django-registration module

class CustomUserCreationForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'twitter_user', 'instagram_user')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'twitter_user', 'instagram_user')