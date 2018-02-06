from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """A user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, null=True, blank=True)

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
    breed = models.CharField(max_length=30)
    profilepic = models.URLField(blank=True, null=True,
                                 verbose_name="profile picture",
                                 help_text="Optional. This will be scaled to a 1:1 aspect ratio.",)
    pic1 = models.URLField(blank=False, null=True, verbose_name="picture 1",
                           help_text="One picture required")
    pic2 = models.URLField(blank=True, null=True, verbose_name="picture 2",)
    pic3 = models.URLField(blank=True, null=True, verbose_name="picture 3",)
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
    dismissed = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    def get24hourtime(self):
        return (str(self.time.hour).zfill(2)
                + ':'
                + str(self.time.minute).zfill(2))

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
