from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from cats.data_cat_breeds import cat_breeds
from timezone_field import TimeZoneField


def cat_picture_path(instance, filename):
    """Return a path to upload a cat picture at.

    This is relative to MEDIA_ROOT.
    """
    userstring = str(instance.owner.user.id)
    return 'user/%s/%s' % (userstring,
                           filename)

class Profile(models.Model):
    """A user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, null=True, blank=True)
    timezone = TimeZoneField(default='Canada/Pacific')

    def __str__(self):
        return "%s" % self.user.username

class Cat(models.Model):
    """A cat."""
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=1,
                           choices=(('F', 'F'),
                                    ('M', 'M'),
                                    ('X', 'X'),),
                           default='F',)
    breed = models.CharField(max_length=30,
                             choices=[(breed, breed) for breed in cat_breeds],
                             default='American Shorthair')
    profilepic = models.ImageField(upload_to=cat_picture_path,
                                   blank=True,
                                   null=True,
                                   verbose_name="profile picture",
                                   help_text="Optional. This will be clipped to a 1:1 aspect ratio.",)
    pic1 = models.ImageField(upload_to=cat_picture_path,
                             blank=False,
                             null=False,
                             verbose_name="picture 1",
                             help_text="Picture 1 is required")
    pic2 = models.ImageField(upload_to=cat_picture_path,
                             blank=True,
                             null=True,
                             verbose_name="picture 2",)
    pic3 = models.ImageField(upload_to=cat_picture_path,
                             blank=True,
                             null=True,
                             verbose_name="picture 3",)
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              null=True)
    votes = models.ManyToManyField('self',
                                   through='Vote',
                                   through_fields=('voter', 'votee'),
                                   symmetrical=False,)

    def __str__(self):
        return "%s [%s, %s] [owner: %s]" % (self.name,
                                            self.sex,
                                            self.breed,
                                            self.owner.user.username,)

class Match(models.Model):
    """A Cat's match(es)."""
    matchingcat = models.ForeignKey(Cat,
                                    on_delete=models.CASCADE,
                                    related_name="matchingcat",
                                    verbose_name="owner's cat",
                                    null=True)
    matchedcat = models.ForeignKey(Cat,
                                   on_delete=models.CASCADE,
                                   related_name="matchedcat",
                                   verbose_name="matched cat",
                                   default=0,)
    time = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

    def get24hourtime(self, the_timezone):
        the_time = timezone.localtime(self.time, timezone=the_timezone)
        return (str(the_time.hour).zfill(2)
                + ':'
                + str(the_time.minute).zfill(2))

class Vote(models.Model):
    """A 'like' upvote or downvote."""
    class Meta:
        unique_together = ('voter', 'votee')

    value = models.IntegerField(blank=False,
                                choices=((1, 1),
                                         (-1, -1),),
                                default=1,)
    voter = models.ForeignKey(Cat,
                              on_delete=models.CASCADE,
                              related_name="voter",
                              default=0,)
    votee = models.ForeignKey(Cat,
                              on_delete=models.CASCADE,
                              related_name="votee",
                              default=0,)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """Updates a user's profile."""
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_delete, sender=Cat)
def remove_cat_photos(sender, instance, *args, **kwargs):
    """Cleanup a cat's pictures after removing cat."""
    for pic in [instance.profilepic,
                instance.pic1,
                instance.pic2,
                instance.pic3]:
        if pic:
            pic.delete()
