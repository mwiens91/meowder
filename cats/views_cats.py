import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_POST
from cats.forms import CatEditForm, CatSignUpForm
from cats.models import Cat, Vote
from cats.views_profile import home


@login_required
def cat_edit(request, catid):
    """Profile sign up page."""
    cat = get_object_or_404(Cat, id=catid)
    if request.method == 'POST':
        form = CatEditForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect(reverse('cathome', kwargs={'catid': catid}))
    else:
        form = CatEditForm(None, instance=cat)
    return render(request, 'editcat.html', {'cat': cat,
                                            'catid': catid,
                                            'form': form})

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
@require_POST
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
@require_POST
def cat_vote(request, votercatid, voteecatid):
    # Check that user is owner of cat
    if not request.user.profile.cat_set.filter(id=votercatid).exists():
        return redirect(error_wrong_cat)

    # Load the cats
    votercat = get_object_or_404(Cat, id=votercatid)
    voteecat = get_object_or_404(Cat, id=voteecatid)

    # Add the vote
    if request.POST['vote'] == 'up':
        vote = 1
    else:
        vote = -1

    # Register the vote
    Vote.objects.create(value=vote, voter=votercat, votee=voteecat)

    return redirect(cat_home, votercatid)

@login_required
def error_wrong_cat(request):
    """Error page for cat not belonging to owner."""
    return render(request, 'errornotyourcat.html')
