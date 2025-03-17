from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Exists, OuterRef

from datetime import datetime

from gesplan.decorators import group_required
from gesplan.commons import get_float, get_or_none, get_param, get_session, set_session, show_exc
from gestion.models import Waste
from .models import Citizen, WasteCitizen


@group_required("admins",)
def index(request):
    return render(request, "index.html")

'''
    CITIZENS
'''
def set_initial_dates(request):
    idate = get_session(request, "s_citizen_idate")
    edate = get_session(request, "s_citizen_edate")
    now = datetime.now()
    if idate == "":
        set_session(request, "s_citizen_idate", now.strftime("%Y-%m-%d"))
    if edate == "":
        set_session(request, "s_citizen_edate", now.strftime("%Y-%m-%d"))
 
def get_citizens(request):
    plate = get_session(request, "s_citizen_plate")
    idate = datetime.strptime("{} 00:00:00".format(get_session(request, "s_citizen_idate")), "%Y-%m-%d %H:%M:%S")
    edate = datetime.strptime("{} 23:59:59".format(get_session(request, "s_citizen_edate")), "%Y-%m-%d %H:%M:%S")
    waste = get_session(request, "s_citizen_waste")
    kwargs = {"date__range": (idate, edate)}
    if plate != "":
        kwargs["plate__icontains"] = plate
    if waste != "":
        waste_list = [item.citizen.id for item in WasteCitizen.objects.filter(waste=waste)]
        kwargs["id__in"] = waste_list 
    #print(kwargs)
    return Citizen.objects.filter(**kwargs)

def get_citizens_context(request):
    return {
        "items": get_citizens(request),
        "waste_list": Waste.objects.all()
    }

@group_required("admins",)
def citizens(request):
    set_initial_dates(request)
    return render(request, "citizens/citizens.html", get_citizens_context(request))

@group_required("admins",)
def citizens_list(request):
    return render(request, "citizens/citizens-list.html", get_citizens_context(request))

@group_required("admins",)
def citizens_search(request):
    set_session(request, "s_citizen_idate", get_param(request.GET, "s_citizen_idate"))
    set_session(request, "s_citizen_edate", get_param(request.GET, "s_citizen_edate"))
    set_session(request, "s_citizen_plate", get_param(request.GET, "s_citizen_plate"))
    set_session(request, "s_citizen_waste", get_param(request.GET, "s_citizen_waste"))
    return render(request, "citizens/citizens-list.html", get_citizens_context(request))

@group_required("admins",)
def citizens_form(request):
    obj_id = get_param(request.GET, "obj_id")
    obj = get_or_none(Citizen, obj_id)
    if obj == None:
        obj = Citizen.objects.create()
    return render(request, "citizens/citizens-form.html", {'obj': obj})

@group_required("admins",)
def citizens_remove(request):
    obj = get_or_none(Citizen, request.GET["obj_id"]) if "obj_id" in request.GET else None
    if obj != None:
        obj.delete()
    return render(request, "citizens/citizens-list.html", get_citizens_context(request))


