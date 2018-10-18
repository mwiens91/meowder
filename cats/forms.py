"""Forms for editing and creating models."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from timezone_field import TimeZoneFormField
from cats.data_countries import countries
from cats.models import Cat, Profile


class ProfileSignUpForm(UserCreationForm):
    """A form to register a new user."""

    location = forms.ChoiceField(choices=countries, initial="CA")
    timezone = TimeZoneFormField(initial="Canada/Pacific")

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "email",
            "location",
            "timezone",
        )


class UserEditForm(forms.ModelForm):
    """A form to edit a user."""

    class Meta:
        model = User
        fields = ("email",)


class ProfileEditForm(forms.ModelForm):
    """A form to edit a profile."""

    class Meta:
        model = Profile
        fields = ("location", "timezone")


class CatEditForm(forms.ModelForm):
    """A form to edit a cat's pictures."""

    class Meta:
        model = Cat
        fields = ("profilepic", "pic1", "pic2", "pic3")

    def __init__(self, *args, **kwargs):
        """Modifies the image fields of a cat."""
        super(CatEditForm, self).__init__(*args, **kwargs)

        # Only show the file input button
        self.fields["profilepic"].widget = forms.FileInput()
        self.fields["pic1"].widget = forms.FileInput()
        self.fields["pic2"].widget = forms.FileInput()
        self.fields["pic3"].widget = forms.FileInput()

        # Don't require the user to change the first picture
        self.fields["pic1"].required = False


class CatSignUpForm(forms.ModelForm):
    """A form to register a new cat."""

    class Meta:
        model = Cat
        fields = ("name", "sex", "breed", "profilepic", "pic1", "pic2", "pic3")
