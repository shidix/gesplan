from django.contrib import admin

from .models import *


class IslandAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class TownAdmin(admin.ModelAdmin):
    list_display = ('name', 'island')

admin.site.register(Island, IslandAdmin)
admin.site.register(Town, TownAdmin)

