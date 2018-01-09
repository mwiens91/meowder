from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cats.models import Cat


class ProfileSignUpForm(UserCreationForm):
    """A form to register a new user."""
    location = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'location', 'email', 'password1', 'password2',)

class CatSignUpForm(forms.ModelForm):
    """A form to register a new cat."""
    class Meta:
        model = Cat
        fields = ('name', 'sex', 'breed',)

    def save(self, commit=True):
        cat = super(CatSignUpForm, self).save(commit=False)

        if commit:
            cat.save()

        return cat
