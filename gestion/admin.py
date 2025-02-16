from django.contrib import admin

from .models import *


class AgreementTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)

class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rol', 'company')
    list_filter = ('rol',)

class EmployeeAccessLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'location', 'finish')

class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)

class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'order', 'operation_time', 'dashboard')

class FacilityActionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'driver', 'fa_type', 'facility', 'truck')

class FacilityActionTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)

#class PriorityAdmin(admin.ModelAdmin):
#    list_display = ('code', 'weight', 'description')

class TrayAdmin(admin.ModelAdmin):
    list_display = ('number',)

class TrayTrackingAdmin(admin.ModelAdmin):
    list_display = ('tray', 'ini_date', 'end_date', 'source', 'target', 'finish')

class TruckTypeAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year')

class WasteAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'external_manager')

class WasteInFacilityAdmin(admin.ModelAdmin):
    list_display = ('code', 'facility', 'waste', 'filling_degree', 'toRoute')
    list_filter = ('facility',)

admin.site.register(AgreementType, AgreementTypeAdmin)
admin.site.register(ContractType, ContractTypeAdmin)
admin.site.register(Company)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeAccessLog, EmployeeAccessLogAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(EmployeeTruck)
admin.site.register(Facility)
admin.site.register(FacilityType, FacilityTypeAdmin)
admin.site.register(FacilityActions, FacilityActionsAdmin)
admin.site.register(FacilityActionType, FacilityActionTypeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Route)
admin.site.register(RouteMpl)
admin.site.register(RouteMplPoint)
admin.site.register(RouteExt)
admin.site.register(Tray, TrayAdmin)
admin.site.register(TrayTracking, TrayTrackingAdmin)
admin.site.register(Truck)
admin.site.register(TruckType, TruckTypeAdmin)
admin.site.register(UnitType)
admin.site.register(Waste, WasteAdmin)
#admin.site.register(Priority, PriorityAdmin)
admin.site.register(WasteInFacility, WasteInFacilityAdmin)

