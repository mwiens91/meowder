from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from cats.forms import ProfileSignUpForm

def homepage(request):
    """The homepage."""
    return render(request, 'homepage.html')

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
            return redirect(homepage)
    else:
        form = ProfileSignUpForm()
    return render(request, 'signup.html', {'form': form})
