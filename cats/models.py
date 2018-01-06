from django.db import models
from django.contrib.auth.models import User

class Cat(models.Model):
    """A cat."""
    breed = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=1,
                           choices=(('F', 'F'),
                                    ('M', 'M'),
                                    ('X', 'X'),),
                           default='F',)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,)
    votes = models.ManyToManyField('self',
                                   through='Vote',
                                   through_fields=('voter', 'votee'),
                                   symmetrical=False,)


    def __str__(self):
        return "%s [%s, %s] " % (self.name, self.sex, self.breed)


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
