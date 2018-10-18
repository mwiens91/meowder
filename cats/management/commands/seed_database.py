"""Contains a utility to seed the database."""

import imp
import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import django_seed
from cats.data_cat_breeds import cat_breeds
from cats.models import Cat, Profile, Vote


# Some data to use for seeds
cat_names = [
    "Alfie",
    "Ashes",
    "Birba",
    "Blacky",
    "Briciola",
    "Caramel",
    "Chanel",
    "Charlie",
    "Charlotte",
    "Charly",
    "Chester",
    "Chicco",
    "Daisy",
    "Eve",
    "Felix",
    "Félix",
    "Ginger",
    "Grisou",
    "Jasper",
    "Kitty",
    "Leo",
    "Lisa",
    "Luna",
    "Max",
    "Micio",
    "Millie",
    "Mimi",
    "Minette",
    "Minka",
    "Minou",
    "Minù",
    "Missy",
    "Misty",
    "Mitten",
    "Molly",
    "Moritz",
    "Muschi",
    "No-rangi-i",
    "Oscar",
    "Pacha",
    "Pallina",
    "Poppy",
    "Puss",
    "Romeo",
    "Smokey",
    "Smudge",
    "Sooty",
    "Susi",
    "Ti-Mine",
    "Tiger",
    "Tigger",
    "Trevor",
    "Trilly",
    "Ya-oong-i",
]
cat_pics = [
    "stock_photos/cat01_01.jpeg",
    "stock_photos/cat02_01.jpeg",
    "stock_photos/cat03_01.jpeg",
    "stock_photos/cat04_01.jpeg",
    "stock_photos/cat05_01.jpeg",
    "stock_photos/cat06_01.jpeg",
    "stock_photos/cat07_01.jpeg",
    "stock_photos/cat08_01.jpeg",
    "stock_photos/cat09_01.jpeg",
    "stock_photos/cat10_01.jpeg",
    "stock_photos/cat11_01.jpeg",
    "stock_photos/cat12_01.jpeg",
    "stock_photos/cat13_01.jpeg",
    "stock_photos/cat14_01.jpeg",
    "stock_photos/cat15_01.jpeg",
    "stock_photos/cat16_01.jpeg",
]


class Command(BaseCommand):
    """This lets us run `./manage.py seed_database`."""

    help = "seed database with fake data"

    def add_arguments(self, parser):
        """Add option to give argument."""
        parser.add_argument("mode", nargs="?", default="small", type=str)

    def handle(self, *args, **options):
        """Execute command with no args."""
        # Make sure the mode passed in is valid
        valid_options = ("large", "medium", "small")

        # Call it with the argument or give an error message
        if options["mode"]:
            mode = options["mode"]

            if mode in valid_options:
                seed_database(mode)
            else:
                raise ValueError("%s is not a valid mode!" % mode)
        else:
            seed_database()


def seed_database(mode="small"):
    """Seeds the Django database with django-seed.

    This function needs to repeatedly reload the django_seed module, so
    that the seeders reset. There might be a better way to do this, but
    there is next to no documentation for the module, and a quick look
    at the source code didn't reveal any solutions.

    Arg:
        mode: A string containing either "large", "medium", or "small"
        which controls how extensively to populate the databse
    """
    # Select how strongly to seed
    if mode == "large":
        N = 30
    elif mode == "medium":
        N = 15
    else:
        N = 5

    # Instantiate some users
    user_seeder = django_seed.Seed.seeder()

    # Not that profiles are auto-created when making a User
    user_seeder.add_entity(User, N, {"is_staff": False})

    # Execute
    user_pks = user_seeder.execute()
    imp.reload(django_seed)

    # Put the new user pks in a list
    user_pks_list = list(user_pks.values())[0]

    # Instantiate some cats
    cat_seeder = django_seed.Seed.seeder()
    cat_seeder.add_entity(
        Cat,
        3 * N // 2,
        {
            "name": lambda x: random.choice(cat_names),
            "sex": lambda x: random.choice(["F", "M", "X"]),
            "breed": lambda x: random.choice(cat_breeds),
            "profilepic": None,
            "pic1": lambda x: random.choice(cat_pics),
            "pic2": None,
            "pic3": None,
            "owner": lambda x: Profile.objects.get(
                user__pk=random.choice(user_pks_list)
            ),
        },
    )

    # Execute
    cat_pks = cat_seeder.execute()
    imp.reload(django_seed)

    # Put the new cat pks in a list
    cat_pks_list = list(cat_pks.values())[0]

    # Instantiate some votes
    all_cats = Cat.objects.all()
    num_votes = len(all_cats) // 3

    for new_cat_pk in cat_pks_list:
        already_voted = []
        this_cat = Cat.objects.get(pk=new_cat_pk)

        for _ in range(num_votes):
            # Make sure we pick a different cat each time
            while True:
                cat_to_vote = random.choice(all_cats)

                if (
                    cat_to_vote != this_cat
                    and cat_to_vote not in already_voted
                ):
                    # Make sure we don't select this cat again
                    already_voted.append(cat_to_vote)
                    break

            # Add a vote
            vote_seeder = django_seed.Seed.seeder()
            vote_seeder.add_entity(
                Vote,
                1,
                {
                    "value": lambda x: random.choice([-1, 1]),
                    "voter": this_cat,
                    "votee": cat_to_vote,
                },
            )
            vote_seeder.execute()
            imp.reload(django_seed)
