from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, render
from cats.forms import ProfileSignUpForm
from cats.models import Profile, Match
import datetime


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
def home(request):
    """The user's main page.

    Renders all of a user's cats and display a notification if there are
    any new matches.
    """
    # Collect the owner's cats
    cats = request.user.profile.cat_set.all()

    # Determine whether to display a notification
    if Match.objects.filter(
                matchingcat__owner__id=request.user.profile.id).filter(
                seen=False).exists():
        shownotification = True
    else:
        shownotification = False

    return render(request, 'home.html', {'cats': cats,
                                         'shownotification': shownotification})

@login_required
def matches(request):
    """The page showing a user's cat's matches.

    Renders a page with all of a user's cat's matches. Passes along a
    dictionary containing dates as keys, and the matches as values.
    Also passes along two strings indicating the current date and
    yesterday's date.
    """
    # A dictionary to store matches, with keys being date strings
    match_dict = dict()

    # Mark any unseen matches as seen
    for unseen_match in Match.objects.filter(
                matchingcat__owner__id=request.user.profile.id).filter(
                seen=False):
        unseen_match.seen = True
        unseen_match.save(update_fields=['seen'])

    # Sort all relevant matches by time
    matches = Match.objects.filter(
                matchingcat__owner__id=request.user.profile.id).order_by(
                '-time')

    # A helper function to convert date objects to strings
    def dateStringify(dateobj):
        dateString = (str(dateobj.year)
                      + '-'
                      + str(dateobj.month).zfill(2)
                      + '-'
                      + str(dateobj.day).zfill(2)
                     )
        return dateString

    # Create a string for today's date and yesterday's date
    todayString = dateStringify(timezone.now())
    yesterdayString = dateStringify(timezone.now() - datetime.timedelta(days=1))

    # Build dictionary by using each match's date as a key
    for match in matches:
        datestring = dateStringify(match.time)
        if datestring in match_dict:
            match_dict[datestring] += [match]
        else:
            match_dict[datestring] = [match]

    return render(request, 'matches.html', {'matchdict': match_dict,
                                            'todaydate': todayString,
                                            'yesterdaydate': yesterdayString})

@login_required
def profile_edit(request):
    """User interface page for editing profile."""
    return render(request, 'editprofile.html')

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
