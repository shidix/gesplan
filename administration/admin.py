from django.contrib import admin

from .models import *


class ContractStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class EpigraphAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

admin.site.register(ContractStatus, ContractStatusAdmin)
admin.site.register(Epigraph, EpigraphAdmin)
#
