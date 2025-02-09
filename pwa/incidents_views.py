from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime

from gesplan.decorators import group_required_pwa
from gesplan.commons import get_or_none, get_param, show_exc
from incidents.models import Incident, IncidentType

import random, string


'''
    INCIDENTS
'''
@group_required_pwa("drivers", "drivers_mpl", "operators")
def incidents(request):
    now = datetime.now()
    idate = now.replace(hour=0, minute=0)
    edate = now.replace(hour=23, minute=59)
    item_list = Incident.objects.filter(owner=request.user, creation_date__range=(idate, edate))
    return render(request, "incidents/incidents.html", {'item_list': item_list})

@group_required_pwa("drivers", "drivers_mpl", "operators")
def incidents_add(request):
    return render(request, "incidents/incidents-form.html", {"type_list": IncidentType.objects.filter(driver=True)})

@group_required_pwa("drivers", "drivers_mpl", "operators")
def incidents_save(request):
    try:
        code =''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
        subject = get_param(request.POST, "subject")
        description = get_param(request.POST, "description")
        itype = get_or_none(IncidentType, get_param(request.POST, "type"))
        Incident.objects.create(code=code, subject=subject, description=description, owner=request.user, type=itype)
        return redirect("pwa-incidents")
    except Exception as e:
        return (render(request, "error_exception.html", {'exc':show_exc(e)}))


