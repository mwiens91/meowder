"""Gives better model visibility to admin section."""

from django.contrib import admin
from cats.models import Cat, Match, Profile, Vote

class MatchInline(admin.TabularInline):
    """Allows us to see a cat's matches on the admin page."""
    model = Match
    fk_name = 'matchingcat'
    extra = 0

class VoteInline(admin.TabularInline):
    """Allows us to see a cat's votes on the admin page."""
    model = Vote
    fk_name = 'voter'
    extra = 0

class CatAdmin(admin.ModelAdmin):
    """Interface modifiers for the Cat model for the admin page."""
    inlines = (VoteInline, MatchInline)
    list_display = ('name', 'sex', 'breed', 'owner')

class ProfileAdmin(admin.ModelAdmin):
    """Interface modifiers for the Profile model for the admin page."""
    list_display = ('__str__', 'location', 'timezone')

class VoteAdmin(admin.ModelAdmin):
    """Interface modifiers for the Vote model for the admin page."""
    list_display = ('voter', 'votee', 'value')

class MatchAdmin(admin.ModelAdmin):
    """Interface modifiers for the Vote model for the admin page."""
    list_display = ('matchingcat', 'matchedcat', 'time', 'seen')

admin.site.register(Cat, CatAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Match, MatchAdmin)
