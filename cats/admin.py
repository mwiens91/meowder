from django.contrib import admin
from .models import Cat, Vote

class VoteInline(admin.TabularInline):
    model = Vote
    fk_name = 'voter'
    extra = 0

class CatAdmin(admin.ModelAdmin):
    inlines = (VoteInline,)

admin.site.register(Cat, CatAdmin)
