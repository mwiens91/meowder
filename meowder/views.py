import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, redirect, render, reverse
from cats.forms import CatEditForm, CatSignUpForm, ProfileSignUpForm
from cats.models import Cat, Profile

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
def cat_edit(request, catid):
    """Profile sign up page."""
    cat = get_object_or_404(Cat, id=catid)
    if request.method == 'POST':
        form = CatEditForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect(reverse('cathome',
                                     kwargs={'catid': catid}))
    else:
        form = CatEditForm(None, instance=cat)
    return render(request, 'editcat.html', {'catid': catid, 'form': form})

@login_required
def cat_home(request, catid):
    """Page for rating cats, with a cat."""
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=catid).exists():
        return redirect(error_wrong_cat)

    # Get the Cat object
    cat = get_object_or_404(Cat, id=catid)

    # Find another Cat to rate
    cat_to_rate = random.choice(Cat.objects.exclude(owner__id=cat.owner.id))
    cat_to_rate_pics = [pic for pic in [cat_to_rate.pic1,
                                        cat_to_rate.pic2,
                                        cat_to_rate.pic3] if pic]

    return render(request, 'cathome.html', {'cat': cat,
                                            'cat_to_rate': cat_to_rate,
                                            'cat_to_rate_pics': cat_to_rate_pics,
                                            'catid': catid},)

@login_required
def cat_remove(request, catid):
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=catid).exists():
        return redirect(error_wrong_cat)

    # Remove the cat
    get_object_or_404(Cat, id=catid).delete()
    return redirect(home)

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
def error_wrong_cat(request):
    """Error page for cat not belonging to owner."""
    return render(request, 'errornotyourcat.html')

@login_required
def home(request):
    """The homepage."""
    cats = request.user.profile.cat_set.all()
    return render(request, 'home.html', {'cats': cats})

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
