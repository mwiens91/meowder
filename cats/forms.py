from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileSignUpForm(UserCreationForm):
    """A form to register a new user."""
    location = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'location', 'email',  'password1', 'password2',)
