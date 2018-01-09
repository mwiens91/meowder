from django.contrib import admin
from .models import Cat, Profile, Vote

class VoteInline(admin.TabularInline):
    model = Vote
    fk_name = 'voter'
    extra = 0

class CatAdmin(admin.ModelAdmin):
    inlines = (VoteInline,)
    list_display = ('name', 'sex', 'breed', 'owner')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'location')

admin.site.register(Cat, CatAdmin)
admin.site.register(Profile, ProfileAdmin)
