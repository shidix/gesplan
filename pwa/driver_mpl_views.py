from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime

from gesplan.decorators import group_required_pwa
from gesplan.commons import get_or_none, get_param, show_exc
from gestion.models import Facility, Waste, WasteInFacility, RouteMpl, RouteMplPoint, FacilityActions


'''
    DRIVERS
'''
@group_required_pwa("drivers_mpl")
def driver_home(request):
    try:
        #if request.user.employee.truck == None:
        #    return redirect(reverse("pwa-driver-select-truck"))
        return redirect(reverse("pwa-driver-mpl-routes"))
        #return render(request, "drivers-mpl/home.html", {"now": datetime.now()})
    except Exception as e:
        return (render(request, "error_exception.html", {'exc':show_exc(e)}))

'''
    ROUTES
'''
@group_required_pwa("drivers_mpl")
def driver_routes(request):
    route = RouteMpl.objects.filter(finish=False).first()
    now = datetime.now()
    idate = now.replace(hour=0, minute=0)
    edate = now.replace(hour=23, minute=59)
    item_list = RouteMpl.objects.filter(driver=request.user.employee, finish=True, ini_date__range=(idate, edate))
    action_list = FacilityActions.objects.filter(driver=request.user.employee, date__range=(idate, edate))
    return render(request, "drivers-mpl/routes.html", {'route': route, 'item_list': item_list, 'action_list': action_list, 'now': now})

@group_required_pwa("drivers_mpl")
def driver_routes_source(request):
    route = RouteMpl.currentRoute(request.user.employee)
    context = {'route': route, 'truck': request.user.employee.truck, "item_list": Facility.getMPL()}
    return render(request, "drivers-mpl/routes-source.html", context)

@group_required_pwa("drivers_mpl")
def driver_routes_wastes(request):
    route = get_or_none(RouteMpl, get_param(request.GET, "route"))
    source = get_or_none(Facility, get_param(request.GET, "value"))
    context = {'item_list': source.waste.filter(toRoute=True), 'source': source, 'route': route}
    return render(request, "drivers-mpl/routes-waste.html", context)

@group_required_pwa("drivers_mpl")
def driver_routes_confirm(request):
    route = get_or_none(RouteMpl, get_param(request.POST, "route"))
    source = get_or_none(Facility, get_param(request.POST, "source"))
    item_list = source.waste.filter(toRoute=True)
    for item in item_list:
        if item.waste != None:
            val = get_param(request.POST, item.waste.code)
            if val != "" and item.waste != None:
                rmp = RouteMplPoint.objects.create(weight=val, mpl=source, waste=item, route=route)
    return redirect(reverse("pwa-driver-mpl-routes"))

@group_required_pwa("drivers_mpl")
def driver_routes_target(request, route):
    r = get_or_none(RouteMpl, route)
    #item_list = Facility.objects.filter(description__icontains="Punto")
    return render(request, "drivers-mpl/routes-target.html", {'route': r, 'item_list': Facility.getPL()})

@group_required_pwa("drivers_mpl")
def driver_routes_finish(request):
    route = get_or_none(RouteMpl, get_param(request.GET, "route"))
    target = get_or_none(Facility, get_param(request.GET, "value"))
    #weight = get_param(request.GET, "weight")
    route.target = target
    #route.weight = weight
    route.save()
    return render(request, "drivers-mpl/routes-finish.html", {'route': route})

@group_required_pwa("drivers_mpl")
def driver_routes_end(request, route):
    try:
        r = get_or_none(RouteMpl, route)
        r.end_date = datetime.now()
        r.finish = True
        r.save()
        return redirect(reverse("pwa-driver-mpl-routes"))
    except Exception as e:
        return (render(request, "error_exception.html", {'exc':show_exc(e)}))


