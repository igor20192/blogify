# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """A form to update user information.

    Attributes:
    - model: The model to use to create the form.
    - fields: The fields of the model that should be included in the form."""

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    """A form to update a user's profile.

    Attributes:
    - model: The model to use to create the form.
    - fields: The model fields that should be included in the form."""

    class Meta:
        model = Profile
        fields = ["avatar"]
