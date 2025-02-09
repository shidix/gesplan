from django.contrib import admin

from .models import *


class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'operator', 'driver')

class IncidentAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'creation_date', 'type', 'owner', 'closed')

admin.site.register(IncidentType, IncidentTypeAdmin)
admin.site.register(Incident, IncidentAdmin)

