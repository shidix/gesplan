from django.http import HttpResponse
from django.shortcuts import render, redirect

from gesplan.decorators import group_required
from gesplan.commons import get_float, get_or_none, get_param, get_session, set_session, show_exc
from .models import Incident, IncidentType


@group_required("admins",)
def index(request):
    return render(request, "index.html")



