from django.contrib import admin
from cats.models import Cat, Profile, Vote

class VoteInline(admin.TabularInline):
    """Allows us to see a cat's votes on admin page."""
    model = Vote
    fk_name = 'voter'
    extra = 0

class CatAdmin(admin.ModelAdmin):
    """Interface modifiers for the Cat model for the admin page."""
    inlines = (VoteInline,)
    list_display = ('name', 'sex', 'breed', 'owner')

class ProfileAdmin(admin.ModelAdmin):
    """Interface modifiers for the Profile model for the admin page."""
    list_display = ('__str__', 'location')

admin.site.register(Cat, CatAdmin)
admin.site.register(Profile, ProfileAdmin)
