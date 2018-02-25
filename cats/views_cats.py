"""Views pertaining to cats."""

import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from cats.forms import CatEditForm, CatSignUpForm
from cats.models import Cat, Match, Vote
from cats.views_profile import home


@never_cache
@login_required
def cat_edit(request, catid):
    """Page to upload new cat pictures."""
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=catid).exists():
        return redirect(error_wrong_cat)

    cat = Cat.objects.get(id=catid)
    if request.method == 'POST':
        form = CatEditForm(request.POST, request.FILES, instance=cat)

        # Remember old pics here so we can remove them if overwritten
        old_pics = [cat.profilepic, cat.pic1, cat.pic2, cat.pic3]

        if form.is_valid():
            # Remove any overwritten pictures
            new_pics = [cat.profilepic, cat.pic1, cat.pic2, cat.pic3]

            for triple in zip(['profilepic', 'pic1', 'pic2', 'pic3'],
                              old_pics,
                              new_pics):
                if triple[1] and triple[1] != triple[2]:
                    triple[1].delete()
                    setattr(cat, triple[0], triple[2])

            # Save the cat
            form.save()

            # If picture 3 exists but not picture 2, swap the pictures
            # (picture 3 will be blank)
            if not cat.pic2 and cat.pic3:
                cat.pic2, cat.pic3 = cat.pic3, cat.pic2
                cat.save()

            return render(request, 'editcat.html', {'cat': cat,
                                                    'catid': catid,
                                                    'form': form})
    else:
        form = CatEditForm(instance=cat)
    return render(request, 'editcat.html', {'cat': cat,
                                            'catid': catid,
                                            'form': form})

@never_cache
@login_required
def cat_home(request, catid):
    """Page for rating cats, with a cat."""
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=catid).exists():
        return redirect(error_wrong_cat)

    # Get the Cat object
    cat = Cat.objects.get(id=catid)

    # Find another Cat to rate - needs a different owner and must have
    # not already been voted
    set_of_cats_to_rate = Cat.objects.exclude(
                owner__id=cat.owner.id).difference(cat.votes.all())

    # Check if there are any cats to rate
    if not set_of_cats_to_rate:
        return render(request, 'cathome_novotes.html', {'cat': cat,
                                                        'catid': catid},)

    # Choose a cat
    cat_to_rate = random.choice(set_of_cats_to_rate)
    cat_to_rate_pics = [pic for pic in [cat_to_rate.pic1,
                                        cat_to_rate.pic2,
                                        cat_to_rate.pic3] if pic]

    # Return the voting page
    return render(request, 'cathome.html', {'cat': cat,
                                            'cat_to_rate': cat_to_rate,
                                            'cat_to_rate_pics': cat_to_rate_pics,
                                            'catid': catid},)

@login_required
@require_POST
def cat_remove(request, catid):
    """Remove a cat."""
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=catid).exists():
        return redirect(error_wrong_cat)

    # Remove the cat
    Cat.objects.get(id=catid).delete()
    return redirect(home)

@never_cache
@login_required
def cat_reorder(request, catid):
    """Page to reorder and delete cat pictures."""
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=catid).exists():
        return redirect(error_wrong_cat)

    # Get the cat
    cat = Cat.objects.get(id=catid)

    if request.method == 'POST':
        # Reorder or remove the pictures. Assume the values given are
        # valid; i.e., leave verification to the template.
        formvals = request.POST

        # Delete the profile picture if selected
        profile_val = formvals.get('profilepic')
        if profile_val == 'delete':
            cat.profilepic.delete()

        # Reorder or delete the rating pictures
        old_pics = [cat.pic1, cat.pic2, cat.pic3]

        for pic_name in enumerate(['pic1', 'pic2', 'pic3']):
            pic_val = formvals.get(pic_name[1])

            if not pic_val:
                continue
            elif pic_val == 'delete':
                # Delete the picture
                old_pics[pic_name[0]].delete()
            elif pic_val != str(pic_name[0] + 1):
                # Reorder the pic
                setattr(cat, 'pic' + pic_val, old_pics[pic_name[0]])

        # Save changes
        cat.save()

    return render(request, 'editcatreorder.html', {'cat': cat,
                                                   'catid': catid})

@never_cache
@login_required
def cat_signup(request):
    """Cat sign up page."""
    if request.method == 'POST':
        # Make a new cat to give to the form so the form knows where to
        # save the cat's pictures
        newcat = Cat()
        newcat.owner = request.user.profile

        form = CatSignUpForm(request.POST, request.FILES, instance=newcat)
        if form.is_valid():
            cat = form.save()
            cat.refresh_from_db()
            cat.owner = request.user.profile

            # If picture 3 provided but not picture 2, swap the pictures
            # (picture 3 will be blank)
            if not cat.pic2 and cat.pic3:
                cat.pic2, cat.pic3 = cat.pic3, cat.pic2

            cat.save()
            return redirect(home)
    else:
        form = CatSignUpForm()
    return render(request, 'catsignup.html', {'form': form})

@login_required
@require_POST
def cat_vote(request, votercatid, voteecatid):
    """Register a vote."""
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=votercatid).exists():
        return redirect(error_wrong_cat)

    # Load the cats
    votercat = Cat.objects.get(id=votercatid)
    voteecat = Cat.objects.get(id=voteecatid)

    # Add the vote
    if request.POST['vote'] == 'up':
        vote = 1
    else:
        vote = -1

    # Register the vote
    Vote.objects.create(value=vote, voter=votercat, votee=voteecat)

    # Add matches if cats are matched
    if vote == 1 and Vote.objects.filter(
                                         voter__id=voteecatid).filter(
                                         votee__id=votercatid).filter(
                                         value=1):
        Match.objects.create(matchingcat=votercat,
                             matchedcat=voteecat)
        Match.objects.create(matchingcat=voteecat,
                             matchedcat=votercat)

    return redirect(cat_home, votercatid)

@login_required
def error_wrong_cat(request):
    """Error page for cat not belonging to owner."""
    return render(request, 'errornotyourcat.html')
