from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from gesplan.decorators import group_required
from gesplan.commons import get_float, get_or_none, get_param, get_session, set_session, show_exc
from .models import Facility, Route
from .views import get_facilities, get_routes


@group_required("admins",)
def index(request):
    #facilities = Facility.objects.filter(description__contains="Punto")
    #facilities_mpl = Facility.objects.filter(code__startswith="MPL-")
    facilities = Facility.getPL()
    facilities_mpl = Facility.getMPL()
    routes = get_routes(request)
    routes_mpl = get_routes(request, "MPL")
    context = {"facilities": facilities, "facilities_mpl": facilities_mpl, "routes": routes, "routes_mpl": routes_mpl}
    return render(request, "operations/index.html", context)

@group_required("admins",)
def facility_waste(request):
    fac = get_or_none(Facility, get_param(request.GET, "obj_id"))
    r = True if get_param(request.GET, "route") == "True" else False
    return render(request, "operations/facility-waste.html", {"item_list": fac.waste.filter(toRoute=r),})
