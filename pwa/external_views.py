from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime

from gesplan.decorators import group_required_pwa
from gesplan.commons import get_or_none, get_param, show_exc, get_float
from gestion.models import RouteExt, WasteInFacility


'''
    EXTERNAL
'''
@group_required_pwa("external")
def external_home(request):
    try:
        return redirect(reverse("pwa-external-wastes"))
        #return redirect(reverse("pwa-external-routes"))
    except Exception as e:
        return (render(request, "error_exception.html", {'exc':show_exc(e)}))

'''
    WASTES
'''
@group_required_pwa("external")
def external_wastes(request):
    print(request.user.employee)
    print(request.user.employee.company)
    item_list = WasteInFacility.objects.filter(waste__external_manager=request.user.employee.company, toRoute=False)
    print(item_list)
    return render(request, "external/wastes.html", {'item_list': item_list,})

'''
    ROUTES
'''
@group_required_pwa("external")
def external_routes(request):
    item_list = RouteExt.objects.filter(external_manager=request.user.employee.company)
    return render(request, "external/routes.html", {'item_list': item_list,})

@group_required_pwa("external")
def external_routes_form(request):
    obj = get_or_none(RouteExt, get_param(request.GET, "obj_id"))
    return render(request, "external/routes-form.html", {'obj': obj,})

@group_required_pwa("external")
def external_routes_save(request):
    try:
        obj = get_or_none(RouteExt, get_param(request.POST, "obj_id"))
        val = get_float(get_param(request.POST, "weight"))
        obj.manager = request.user.employee
        obj.get_date = datetime.now()
        obj.weight = val
        obj.save()
        return redirect("pwa-external")
    except Exception as e:
        return HttpResponse(e)


