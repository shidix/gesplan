from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from gesplan.decorators import group_required_pwa
from gesplan.commons import get_or_none, get_param, show_exc
from gestion.models import Facility, FacilityActions, FacilityActionType


'''
    ACTIONS
'''
@group_required_pwa("drivers", "drivers_mpl")
def actions(request):
    #now = datetime.now()
    #idate = now.replace(hour=0, minutes=0)
    #edate = now.replace(hour=23, minutes=59)
    fac_list = Facility.getPL()
    action_list = FacilityActionType.objects.all()
    #fa_list = FacilityActions.objects.filter(driver=request.user.driver, date__range=(idate, edate))
    return render(request, "actions/actions.html", {'action_list': action_list, 'fac_list': fac_list})

@group_required_pwa("drivers", "drivers_mpl")
def save_action(request):
    try:
        fac = get_or_none(Facility, get_param(request.POST, "facility"))
        action = get_or_none(FacilityActionType, get_param(request.POST, "action"))
        if fac != "" and action != "":
            emp = request.user.employee
            fa = FacilityActions.objects.create(facility=fac, fa_type=action, driver=emp, truck=emp.truck)
            return redirect("pwa-home")
        else:
            return (render(request, "error_exception.html", {'exc': 'Facility or Action not found!'}))
    except Exception as e:
        return (render(request, "error_exception.html", {'exc':show_exc(e)}))

