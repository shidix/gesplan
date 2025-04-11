from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime

from gesplan.decorators import group_required
from gesplan.commons import get_float, get_or_none, get_param, get_session, set_session, show_exc
from .models import Facility, Route, RouteExt, Waste, Company
from .views import get_facilities


@group_required("admins",)
def index(request):
    #facilities = Facility.objects.filter(description__contains="Punto")
    #facilities_mpl = Facility.objects.filter(code__startswith="MPL-")
    facilities = Facility.getPL()
    facilities_mpl = Facility.getMPL()
    routes = get_routes(request)
    routes_mpl = get_routes(request, "MPL")
    routes_ext = RouteExt.objects.all()
    context = {"facilities":facilities,"facilities_mpl":facilities_mpl,"routes":routes,"routes_mpl":routes_mpl,"routes_ext":routes_ext}
    return render(request, "operations/index.html", context)

@group_required("admins",)
def facility_waste(request):
    fac = get_or_none(Facility, get_param(request.GET, "obj_id"))
    r = True if get_param(request.GET, "route") == "True" else False
    return render(request, "operations/facility-waste.html", {"item_list": fac.waste.filter(toRoute=r),})

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
    return Route.objects.filter(full_query).filter(code=code)[:30]

@group_required("admins",)
def routes_view(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Route, obj_id)
    if obj == None:
        obj = Route.objects.create()
    return render(request, "operations/routes-view.html", {'obj': obj})

@group_required("admins",)
def routes_list(request):
    return render(request, "operations/routes/routes-list.html", {"items": get_routes(request)})

@group_required("admins",)
def routes_ext_list(request):
    return render(request, "operations/routes/routes-list.html", {"items": RouteExt.objects.all()})

#@group_required("admins",)
#def routes_form(request):
#    obj_id = get_param(request.GET, "obj_id")
#    obj = get_or_none(Route, obj_id)
#    if obj == None:
#        obj = Route.objects.create()
#    return render(request, "operations/routes/routes-form.html", {'obj': obj})

@group_required("admins",)
def routes_ext_form(request):
    obj = get_or_none(RouteExt, get_param(request.GET, "obj_id"))
    #if obj == None:
    #    obj = RouteExt.objects.create()
    return render(request, "operations/routes/routes-ext-form.html", {'obj': obj})

@group_required("admins",)
def routes_remove(request):
    obj = get_or_none(Route, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "operations/routes/routes-list.html", {"items": get_routes(request)})

'''
    OPERATIONS REPORTS
'''
def get_operation_report(request):
    idate_ini = datetime.strptime(get_session(request, "sr_operation_idate_ini"), "%Y-%m-%d")
    idate_end = get_session(request, "sr_operation_idate_end")
    edate_ini = get_session(request, "sr_operation_edate_ini")
    edate_end = get_session(request, "sr_operation_edate_end")
    waste = get_session(request, "sr_operation_waste")
    comp = get_session(request, "sr_operation_comp")
    fac = get_session(request, "sr_operation_fac")
    target = get_session(request, "sr_operation_target")
    plate = get_session(request, "sr_operation_plate")

    kwargs = {"code": "PL"}
    if idate_ini != "":
        kwargs["ini_date__gte"] = idate_ini
    if idate_end != "":
        kwargs["ini_date__lte"] = idate_end
    if edate_ini != "":
        kwargs["end_date__gte"] = edate_ini
    if edate_end != "":
        kwargs["end_date__lte"] = edate_end
    if waste != "":
        kwargs["waste__waste__id"] = waste
    if comp != "":
        kwargs["driver__company__id"] = comp
    if fac != "":
        kwargs["source__id"] = comp
    if target != "":
        kwargs["target__id"] = comp
    if plate != "":
        kwargs["truck__number_plate__icontains"] = comp
    print(kwargs)
    return Route.objects.filter(**kwargs)

@group_required("admins",)
def report(request):
    context = {"items":[], "waste_list":Waste.objects.all(), "comp_list":Company.objects.all(), "fac_list":Facility.getPL(),}
    return render(request, "operations/reports/operations.html", context)

@group_required("admins",)
def report_search(request):
    set_session(request, "sr_operation_idate_ini", get_param(request.GET, "sr_operation_idate_ini"))
    set_session(request, "sr_operation_idate_end", get_param(request.GET, "sr_operation_idate_end"))
    set_session(request, "sr_operation_edate_ini", get_param(request.GET, "sr_operation_edate_ini"))
    set_session(request, "sr_operation_edate_end", get_param(request.GET, "sr_operation_edate_end"))
    set_session(request, "sr_operation_waste", get_param(request.GET, "sr_operation_waste"))
    set_session(request, "sr_operation_comp", get_param(request.GET, "sr_operation_comp"))
    set_session(request, "sr_operation_fac", get_param(request.GET, "sr_operation_fac"))
    set_session(request, "sr_operation_target", get_param(request.GET, "sr_operation_target"))
    set_session(request, "sr_operation_plate", get_param(request.GET, "sr_operation_plate"))
    return render(request, "operations/reports/operations-list.html", {"items": get_operation_report(request)})


'''
    Externals
'''
@group_required("external",)
def index_external(request):
    items = RouteExt.objects.filter(external_manager=request.user.employee.company)
    return render(request, "operations/external/index.html", {"routes_ext": items})

@group_required("external",)
def routes_external_list(request):
    items = RouteExt.objects.filter(external_manager=request.user.employee.company)
    return render(request, "operations/external/routes-list.html", {"items": items})

@group_required("external",)
def routes_external_form(request):
    obj = get_or_none(RouteExt, get_param(request.GET, "obj_id"))
    if obj == None:
        obj = RouteExt.objects.create(external_manager=request.user.employee.company)
    return render(request, "operations/external/routes-ext-form.html", {'obj': obj})


