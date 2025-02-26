from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from datetime import datetime

from gesplan.decorators import group_required
from gesplan.commons import get_int, get_float, get_or_none, get_param, get_session, set_session, show_exc
from .models import Company, Facility, Truck, Employee, EmployeeType, Route, Item, EmployeeItem
from .models import EmployeeContract, ContractType, AgreementType, FacilityItem


@group_required("admins",)
def index(request):
    return render(request, "index.html")


'''
    COMPANIES
'''
def get_companies(request):
    search_value = get_session(request, "s-comp-name")
    filters_to_search = ["name__icontains",]
    full_query = Q()
    if search_value != "":
        for myfilter in filters_to_search:
            full_query |= Q(**{myfilter: search_value})
    return Company.objects.filter(full_query)

@group_required("admins",)
def companies(request):
    return render(request, "companies/companies.html", {"items": get_companies(request)})

@group_required("admins",)
def companies_list(request):
    return render(request, "companies/companies-list.html", {"items": get_companies(request)})

@group_required("admins",)
def companies_search(request):
    search_value = get_param(request.GET, "s-name")
    set_session(request, "s-comp-name", search_value)
    return render(request, "companies/companies-list.html", {"items": get_companies(request)})

@group_required("admins",)
def companies_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Company, obj_id)
    if obj == None:
        obj = Company.objects.create()
    return render(request, "companies/companies-form.html", {'obj': obj})

@group_required("admins",)
def companies_remove(request):
    obj = get_or_none(Company, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "companies/companies-list.html", {"items": get_companies(request)})

'''
    FACILITIES
'''
def get_facilities(request):
    search_value = get_session(request, "s-facility-name")
    filters_to_search = ["name__icontains",]
    full_query = Q()
    if search_value != "":
        for myfilter in filters_to_search:
            full_query |= Q(**{myfilter: search_value})
    return Facility.objects.filter(full_query)

@group_required("admins",)
def facilities(request):
    return render(request, "facilities/facilities.html", {"items": get_facilities(request)})

@group_required("admins",)
def facilities_list(request):
    return render(request, "facilities/facilities-list.html", {"items": get_facilities(request)})

@group_required("admins",)
def facilities_search(request):
    search_value = get_param(request.GET, "s-name")
    set_session(request, "s-facility-name", search_value)
    return render(request, "facilities/facilities-list.html", {"items": get_facilities(request)})

@group_required("admins",)
def facilities_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Facility, obj_id)
    if obj == None:
        obj = Facility.objects.create()
    return render(request, "facilities/facilities-form.html", {'obj': obj})

@group_required("admins",)
def facilities_remove(request):
    obj = get_or_none(Facility, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "facilities/facilities-list.html", {"items": get_facilities(request)})

'''
    FACILITIES ITEMS
'''
@group_required("admins",)
def facilities_items(request):
    obj = get_or_none(Facility, request.GET["obj_id"])
    return render(request, "facilities/facilities-items.html", {"obj": obj, "item_list": Item.objects.all()})

@group_required("admins",)
def facilities_items_add(request):
    obj = get_or_none(Facility, get_param(request.POST, "facility"))
    item = get_or_none(Item, get_param(request.POST, "item"))
    amount = get_int(get_param(request.POST, "amount"))
    desc = get_param(request.POST, "desc")
    FacilityItem.objects.create(facility=obj, item=item, amount=amount, desc=desc)
    return render(request, "facilities/facilities-items-list.html", {"obj": obj, "item_list": Item.objects.all()})

@group_required("admins",)
def facilities_items_return(request):
    obj = get_or_none(FacilityItem, get_param(request.GET, "obj_id"))
    obj.return_date = datetime.now()
    obj.returned = True
    obj.save()
    return render(request, "facilities/facilities-items-list.html", {"obj": obj, "item_list": Item.objects.all()})

@group_required("admins",)
def facilities_items_remove(request):
    obj = get_or_none(FacilityItem, get_param(request.GET, "obj_id"))
    fac = None
    if obj != None:
        fac = obj.facility
        obj.delete()
    return render(request, "facilities/facilities-items-list.html", {"obj": fac, "item_list": Item.objects.all()})

'''
    TRUCKS
'''
def get_trucks(request):
    search_value = get_session(request, "s-truck-name")
    filters_to_search = ["name__icontains",]
    full_query = Q()
    if search_value != "":
        for myfilter in filters_to_search:
            full_query |= Q(**{myfilter: search_value})
    return Truck.objects.filter(full_query)

@group_required("admins",)
def trucks(request):
    return render(request, "trucks/trucks.html", {"items": get_trucks(request)})

@group_required("admins",)
def trucks_list(request):
    return render(request, "trucks/trucks-list.html", {"items": get_trucks(request)})

@group_required("admins",)
def trucks_search(request):
    search_value = get_param(request.GET, "s-name")
    set_session(request, "s-truck-name", search_value)
    return render(request, "trucks/trucks-list.html", {"items": get_trucks(request)})

@group_required("admins",)
def trucks_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Truck, obj_id)
    if obj == None:
        obj = Truck.objects.create()
    return render(request, "trucks/trucks-form.html", {'obj': obj, 'facilities': Facility.getPL()})

@group_required("admins",)
def trucks_remove(request):
    obj = get_or_none(Truck, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "trucks/trucks-list.html", {"items": get_trucks(request)})

'''
    ROUTES
'''
def get_routes(request, code="PL"):
    search_value = get_session(request, "s-truck-name")
    filters_to_search = ["name__icontains",]
    full_query = Q()
    if search_value != "":
        for myfilter in filters_to_search:
            full_query |= Q(**{myfilter: search_value})
    return Route.objects.filter(full_query).filter(code=code)

@group_required("admins",)
def routes(request):
    return render(request, "routes/routes.html", {"items": get_routes(request)})

@group_required("admins",)
def routes_list(request):
    return render(request, "routes/routes-list.html", {"items": get_routes(request)})

@group_required("admins",)
def routes_search(request):
    search_value = get_param(request.GET, "s-name")
    set_session(request, "s-truck-name", search_value)
    return render(request, "routes/routes-list.html", {"items": get_routes(request)})

@group_required("admins",)
def routes_view(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Route, obj_id)
    if obj == None:
        obj = Route.objects.create()
    return render(request, "routes/routes-view.html", {'obj': obj})

@group_required("admins",)
def routes_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Route, obj_id)
    if obj == None:
        obj = Route.objects.create()
    return render(request, "routes/routes-form.html", {'obj': obj})

@group_required("admins",)
def routes_remove(request):
    obj = get_or_none(Route, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "routes/routes-list.html", {"items": get_routes(request)})

'''
    EMPLOYEES
'''
def get_employees(request):
    search_value = get_session(request, "s_emp_name")
    rol = get_session(request, "s_emp_rol", "operator")
    filters_to_search = ["name__icontains",]
    full_query = Q()
    if search_value != "":
        for myfilter in filters_to_search:
            full_query |= Q(**{myfilter: search_value})
    return Employee.objects.filter(full_query).filter(rol__code=rol)

@group_required("admins",)
def employees(request):
    return render(request, "employees/employees.html", {"items": get_employees(request), 'rol_list': EmployeeType.objects.all()})

@group_required("admins",)
def employees_list(request):
    if "rol" in request.GET:
        set_session(request, "s_emp_rol", get_param(request.GET, "rol"))
    return render(request, "employees/employees-list.html", {"items": get_employees(request)})

@group_required("admins",)
def employees_search(request):
    search_value = get_param(request.GET, "s_emp_name")
    set_session(request, "s_emp_name", search_value)
    return render(request, "employees/employees-list.html", {"items": get_employees(request)})

@group_required("admins",)
def employees_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Employee, obj_id)
    #if obj == None:
    #    obj = Employee.objects.create()
    context = {'obj': obj, 'rol_list': EmployeeType.objects.all(), 'fac_list': Facility.getPL()}
    return render(request, "employees/employees-form.html", context)

@group_required("admins",)
def employees_save(request):
    obj_id = get_param(request.POST, "obj_id")
    obj = get_or_none(Employee, obj_id)
    if obj == None:
        obj = Employee.objects.create()
    obj.name = get_param(request.POST, "name")
    obj.surname = get_param(request.POST, "surname")
    obj.rol = get_or_none(EmployeeType, get_param(request.POST, "rol"))
    obj.facility = get_or_none(Facility, get_param(request.POST, "facility"))
    obj.active = True if get_param(request.POST, "active") != "" else False
    obj.code = get_param(request.POST, "code")
    obj.pin = get_param(request.POST, "pin")
    obj.nif = get_param(request.POST, "nif")
    obj.cellphone = get_param(request.POST, "cellphone")
    obj.device_uid = get_param(request.POST, "device_uid")
    obj.email = get_param(request.POST, "email")
    obj.save()
    obj.save_user()
    return render(request, "employees/employees-list.html", {"items": get_employees(request)})

@group_required("admins",)
def employees_remove(request):
    obj = get_or_none(Employee, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        if obj.user != None:
            obj.user.delete()
        obj.delete()
    return render(request, "employees/employees-list.html", {"items": get_employees(request)})

'''
    EMPLOYEES ITEMS
'''
@group_required("admins",)
def employees_items(request):
    obj = get_or_none(Employee, request.GET["obj_id"])
    return render(request, "employees/employees-items.html", {"obj": obj, "item_list": Item.objects.all()})

@group_required("admins",)
def employees_items_add(request):
    obj = get_or_none(Employee, get_param(request.POST, "employee"))
    item = get_or_none(Item, get_param(request.POST, "item"))
    amount = get_int(get_param(request.POST, "amount"))
    desc = get_param(request.POST, "desc")
    EmployeeItem.objects.create(employee=obj, item=item, amount=amount, desc=desc)
    return render(request, "employees/employees-items-list.html", {"obj": obj, "item_list": Item.objects.all()})

@group_required("admins",)
def employees_items_return(request):
    obj = get_or_none(EmployeeItem, get_param(request.GET, "obj_id"))
    obj.return_date = datetime.now()
    obj.returned = True
    obj.save()
    return render(request, "employees/employees-items-list.html", {"obj": obj.employee, "item_list": Item.objects.all()})

@group_required("admins",)
def employees_items_remove(request):
    obj = get_or_none(EmployeeItem, get_param(request.GET, "obj_id"))
    emp = None
    if obj != None:
        emp = obj.employee
        obj.delete()
    return render(request, "employees/employees-items-list.html", {"obj": emp, "item_list": Item.objects.all()})

'''
    EMPLOYEES CONTRACT
'''
@group_required("admins",)
def employees_contracts(request):
    obj = get_or_none(Employee, request.GET["obj_id"])
    context = {"obj": obj, "contract_list": ContractType.objects.all(), "agreement_list": AgreementType.objects.all()}
    return render(request, "employees/employees-contracts.html", context)

@group_required("admins",)
def employees_contracts_add(request):
    obj = get_or_none(Employee, get_param(request.POST, "employee"))
    contract_type = get_or_none(ContractType, get_param(request.POST, "contract_type"))
    agreement_type = get_or_none(AgreementType, get_param(request.POST, "agreement_type"))
    ec = EmployeeContract.objects.create(employee=obj, contract_type=contract_type, agreement_type=agreement_type)
    if request.POST["ini_date"] != "":
        ec.ini_date = get_param(request.POST, "ini_date")
    if request.POST["end_date"] != "":
        ec.end_date = get_param(request.POST, "end_date")
    ec.timetable = get_param(request.POST, "timetable")
    ec.save()
    return render(request, "employees/employees-contracts-list.html", {"obj": obj,})

@group_required("admins",)
def employees_contracts_remove(request):
    obj = get_or_none(EmployeeContract, get_param(request.GET, "obj_id"))
    emp = None
    if obj != None:
        emp = obj.employee
        obj.delete()
    return render(request, "employees/employees-contracts-list.html", {"obj": emp,})

'''
    ITEMS
'''
def get_items(request):
    search_value = get_session(request, "s-item-name")
    filters_to_search = ["name__icontains",]
    full_query = Q()
    if search_value != "":
        for myfilter in filters_to_search:
            full_query |= Q(**{myfilter: search_value})
    return Item.objects.filter(full_query)

@group_required("admins",)
def items(request):
    return render(request, "items/items.html", {"items": get_items(request)})

@group_required("admins",)
def items_list(request):
    return render(request, "items/items-list.html", {"items": get_items(request)})

@group_required("admins",)
def items_search(request):
    search_value = get_param(request.GET, "s-item-name")
    set_session(request, "s-item-name", search_value)
    return render(request, "items/items-list.html", {"items": get_items(request)})

@group_required("admins",)
def items_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Item, obj_id)
    if obj == None:
        obj = Item.objects.create()
    return render(request, "items/items-form.html", {'obj': obj})

@group_required("admins",)
def items_remove(request):
    obj = get_or_none(Item, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "items/items-list.html", {"items": get_items(request)})

@group_required("admins",)
def items_location(request):
    obj = get_or_none(Item, get_param(request.GET, "obj_id"))
    return render(request, "items/items-location.html", {'obj': obj})


