from django.contrib import admin

from .models import *


class IslandAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class TownAdmin(admin.ModelAdmin):
    list_display = ('name', 'island')

class CitizenRegisterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'identification', 'address', 'usual_plate', 'phone', 'email', 'uuid', 'town', 'postcode')
    search_fields = ('first_name', 'last_name', 'identification')
    list_filter = ('town',)
    list_per_page = 25

class CitizenAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'identification', 'plate', 'facility', 'date')
    search_fields = ('identification', 'plate')
    list_filter = ('facility',)
    ordering = ('-date',)
    list_per_page = 25        

    def full_name(self, obj):
        if obj.getCitizenRegister():
            return "%s, %s" % (obj.getCitizenRegister().last_name, obj.getCitizenRegister().first_name)
        else:
            return obj.identification
    full_name.short_description = 'Ciudadano'

class WasteCitizenAdmin(admin.ModelAdmin):
    list_display = ('units', 'waste', 'citizen__identification', 'citizen__date')
    search_fields = ('citizen__identification', 'waste__name')
    list_filter = ('waste',)
    ordering = ('-units',)
    list_per_page = 25

class CertificateAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'citizen__identification', 'start_date', 'end_date', 'creation_date')
    ordering = ('-creation_date',)
    list_per_page = 25
    


admin.site.register(Island, IslandAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(CitizenRegister, CitizenRegisterAdmin)
admin.site.register(Citizen, CitizenAdmin)
admin.site.register(WasteCitizen, WasteCitizenAdmin)
admin.site.register(Certificate, CertificateAdmin)
