from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, render
from cats.forms import CatSignUpForm, ProfileSignUpForm
from cats.models import Profile

class EditEmail(UpdateView):
    """User interface to editing email."""
    model = User
    fields = ['email']

    def get_object(self, queryset=None):
        return self.request.user

class EditLocation(UpdateView):
    """User interface to editing location."""
    model = Profile
    fields = ['location']

    def get_object(self, queryset=None):
        return self.request.user.profile

@login_required
def cat_signup(request):
    """Cat sign up page."""
    if request.method == 'POST':
        form = CatSignUpForm(request.POST)
        if form.is_valid():
            cat = form.save()
            cat.refresh_from_db()
            cat.owner = request.user.profile
            cat.save()
            return redirect(home)
    else:
        form = CatSignUpForm()
    return render(request, 'catsignup.html', {'form': form})

@login_required
def home(request):
    """The homepage."""
    return render(request, 'home.html')

def profile_signup(request):
    """Profile sign up page."""
    if request.method == 'POST':
        form = ProfileSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(home)
    else:
        form = ProfileSignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_profile(request):
    """User interface to editing profile."""
    return render(request, 'userprofile.html')
