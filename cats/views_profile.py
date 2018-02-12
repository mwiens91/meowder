"""Views pertaining to profiles and matches."""

import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from cats.forms import ProfileEditForm, ProfileSignUpForm, UserEditForm
from cats.models import Cat, Match


@login_required
def error_wrong_match(request):
    """Error page for match not belonging to owner."""
    return render(request, 'errornotyourmatch.html')

@login_required
def home(request):
    """The user's main page.

    Renders all of a user's cats and display a notification if there are
    any new matches. Passes along a dictionary containing cats with
    votes remaining wth cat ids as keys and remaining votes as values;
    abbreviates number of votes > 99 to 99+.
    """
    # Collect the owner's cats
    cats = request.user.profile.cat_set.all()

    # Collect the owner's cats' votes left
    catsvotesleft = dict()

    for cat in cats:
        votes = Cat.objects.exclude(owner__id=cat.owner.id).difference(
                                                        cat.votes.all())
        if votes:
            numvotes = len(votes)

            if numvotes > 99:
                catsvotesleft[cat.id] = "99+"
            else:
                catsvotesleft[cat.id] = str(numvotes)

    # Determine whether to display a notification
    shownotification = bool(
                Match.objects.filter(
                matchingcat__owner__id=request.user.profile.id).filter(
                seen=False).exists())

    return render(request, 'home.html', {'cats': cats,
                                         'catsvotesleft': catsvotesleft,
                                         'shownotification': shownotification})

@login_required
@require_POST
def match_remove(request, matchid):
    """Remove a match."""
    # Check that user is owner of the cat involved in the match
    if not Match.objects.filter(
       matchingcat__owner__id=request.user.profile.id).filter(
       id=matchid):
        return redirect(error_wrong_match)

    # Remove the match
    Match.objects.get(id=matchid).delete()

    # Give back JSON if that's what request is expecting, otherwise just
    # go back to matches page
    if request.META['HTTP_ACCEPT'] == 'application/json':
        return JsonResponse({'matchid': matchid}, status=200)

    return redirect(matches)

@login_required
def matches(request):
    """The page showing a user's cat's matches.

    Renders a page with all of a user's cat's matches. Passes along a
    dictionary containing dates as keys, and the matches as values.
    Also passes along two strings indicating the current date and
    yesterday's date.
    """
    # Get users timezone
    this_timezone = request.user.profile.timezone

    # A dictionary to store matches, with keys being date strings
    match_dict = dict()

    # Mark any unseen matches as seen
    for unseen_match in Match.objects.filter(
                matchingcat__owner__id=request.user.profile.id).filter(
                seen=False):
        unseen_match.seen = True
        unseen_match.save(update_fields=['seen'])

    # Sort all relevant matches by time
    matches_ = Match.objects.filter(
                matchingcat__owner__id=request.user.profile.id).order_by(
                '-time')

    # A helper function to convert date objects to strings
    def dateStringify(dateobj):
        """Convert a date object to an ISO 8601 date string."""
        dateString = (str(dateobj.year)
                      + '-'
                      + str(dateobj.month).zfill(2)
                      + '-'
                      + str(dateobj.day).zfill(2)
                     )
        return dateString

    # Create a string for today's date and yesterday's date
    today = timezone.localtime(timezone.now(), timezone=this_timezone)
    todayString = dateStringify(today)
    yesterdayString = dateStringify(today - datetime.timedelta(days=1))

    # Build dictionary by using each match's date as a key
    for match in matches_:
        datestring = dateStringify(timezone.localtime(match.time,
                                                      timezone=this_timezone))
        if datestring in match_dict:
            match_dict[datestring] += [match]
        else:
            match_dict[datestring] = [match]

    return render(request, 'matches.html', {'matchdict': match_dict,
                                            'todaydate': todayString,
                                            'yesterdaydate': yesterdayString,
                                            'thistimezone': this_timezone})

@login_required
def profile_edit(request):
    """Page to edit user profile.

    Allows editing of email, location, and timezone.
    """
    if request.method == 'POST':
        user_form = UserEditForm(request.POST,
                                 instance=request.user)
        profile_form = ProfileEditForm(request.POST,
                                       instance=request.user.profile)

        # Validate and save
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(home)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'editprofile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,})

def profile_signup(request):
    """Profile sign up page."""
    if request.method == 'POST':
        form = ProfileSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.location = form.cleaned_data.get('location')
            user.profile.timezone = form.cleaned_data.get('timezone')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(home)
    else:
        form = ProfileSignUpForm()
    return render(request, 'signup.html', {'form': form})
