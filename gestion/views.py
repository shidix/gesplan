from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from gesplan.decorators import group_required
from gesplan.commons import get_float, get_or_none, get_param, get_session, set_session, show_exc
from .models import Company, Facility, Truck, Employee, EmployeeType, Route


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
    search_value = get_session(request, "s-emp-name")
    filters_to_search = ["name__icontains",]
    full_query = Q()
    if search_value != "":
        for myfilter in filters_to_search:
            full_query |= Q(**{myfilter: search_value})
    return Employee.objects.filter(full_query)

@group_required("admins",)
def employees(request):
    return render(request, "employees/employees.html", {"items": get_employees(request)})

@group_required("admins",)
def employees_list(request):
    return render(request, "employees/employees-list.html", {"items": get_employees(request)})

@group_required("admins",)
def employees_search(request):
    search_value = get_param(request.GET, "s-name")
    set_session(request, "s-comp-name", search_value)
    return render(request, "employees/employees-list.html", {"items": get_employees(request)})

@group_required("admins",)
def employees_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Employee, obj_id)
    if obj == None:
        obj = Employee.objects.create()
    return render(request, "employees/employees-form.html", {'obj': obj, 'rol_list': EmployeeType.objects.all()})

@group_required("admins",)
def employees_remove(request):
    obj = get_or_none(Employee, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "employees/employees-list.html", {"items": get_employees(request)})


