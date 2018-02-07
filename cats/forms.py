from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from timezone_field import TimeZoneFormField
from cats.models import Cat


class ProfileSignUpForm(UserCreationForm):
    """A form to register a new user."""
    location = forms.CharField(max_length=30)
    timezone = TimeZoneFormField(initial='Canada/Pacific')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email',  'location', 'timezone')

class CatEditForm(forms.ModelForm):
    """A form to edit a cat's pictures."""
    class Meta:
        model = Cat
        fields = ('pic1', 'pic2', 'pic3')

class CatSignUpForm(forms.ModelForm):
    """A form to register a new cat."""
    class Meta:
        model = Cat
        fields = ('name', 'sex', 'breed', 'profilepic', 'pic1', 'pic2', 'pic3')
