from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Exists, OuterRef, Sum


from datetime import datetime, timedelta

from gesplan.decorators import group_required
from gesplan.commons import get_float, get_or_none, get_param, get_session, set_session, show_exc
from gestion.models import Waste
from .models import Citizen, WasteCitizen, CitizenRegister, Facility
from .forms import *



@group_required("admins",)
def index(request):
    set_initial_dates(request)
    return render(request, "report-index.html", get_citizens_context(request))

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
    fac = get_session(request, "s_citizen_facility")
    kwargs = {"date__range": (idate, edate)}
    if plate != "":
        kwargs["plate__icontains"] = plate
    if waste != "":
        waste_list = [item.citizen.id for item in WasteCitizen.objects.filter(waste=waste)]
        kwargs["id__in"] = waste_list 
    if fac != "":
        kwargs["facility__id"] = fac
    #print(kwargs)
    return Citizen.objects.filter(**kwargs)

def get_citizens_context(request):
    return {
        "items": get_citizens(request),
        "waste_list": Waste.objects.all(),
        "facility_list": Facility.getPL()
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
    set_session(request, "s_citizen_facility", get_param(request.GET, "s_citizen_facility"))
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

def citizens_report(request, uuid=None):
    try: 
        if request.method == "POST":    
            uuid = request.POST.get("uuid", None)
            if uuid is None:
               return redirect("pwa-login")
            if uuid == "0000-0000-00000-00000":
                import random

                start_date_str = request.POST.get("start_date", datetime.now().strftime("%Y-%m-%d"))
                # Fake citizen register for testing
                citizen_register = CitizenRegister(
                    uuid=uuid,
                    first_name="Test",
                    last_name="Citizen",
                    identification="12345678Z",
                    address="Test Address",
                    usual_plate="ABC123",
                    phone="600000000",
                    email="none@none.com",
                    town=random.choice(Town.objects.all()),
                    postcode = f'{random.randint(38000, 38999)}'
                )



                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
                end_date_str = request.POST.get("end_date", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                waste_list = Waste.objects.all()
                # Simulate random data for testing
                test_data = []
                for idx in range(random.randint(20, 1000)):
                    fake_date = start_date + timedelta(days = random.randint(0, int((end_date.timestamp() - start_date.timestamp()) / 86400)))
                    waste = random.choice(waste_list)
                    test_data.append({
                        'name': waste.name,
                        'units': waste.units,
                        'date': fake_date,
                        'total_units': random.randint(1, 100),
                    })
                # Sort test data by date
                test_data.sort(key=lambda x: x['date'])
                context = {'uuid': uuid, 'start_date': start_date, 'end_date': end_date, 'items': test_data, 'citizen': citizen_register}
                
                return render(request, "citizens/citizens-report.html", context)                            
            if (CitizenRegister.objects.filter(uuid=uuid).exists()):
                citizen_register = CitizenRegister.objects.get(uuid=uuid)
                start_date_str = request.POST.get("start_date", datetime.now().strftime("%Y-%m-%d"))
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
                end_date_str = request.POST.get("end_date", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                deliveries = Citizen.objects.filter(identification=citizen_register.identification, date__range=(start_date, end_date))
                if deliveries.exists():
                    ## Get WasteCitizen objects grouped by waste
                    waste_citizen = WasteCitizen.objects.filter(citizen__identification=citizen_register.identification, citizen__date__range=(start_date, end_date))
                    waste_list = Waste.objects.filter(id__in=waste_citizen.values_list('waste', flat=True)).distinct()
                    waste_list = waste_list.annotate(total_units=Sum('wastecitizen__units')).order_by('name')
                    context = {'uuid': uuid, 'start_date': start_date, 'end_date': end_date, 'items': waste_list, 'citizen': citizen_register}



                context = {'uuid': uuid, 'start_date': start_date, 'end_date': end_date}
                return render(request, "citizens/citizens-report.html", context)
        else:

            if uuid is not None:
                if (uuid == '0000-0000-00000-00000'):
                    start_date = (datetime.now() - timedelta(days=30)).replace(hour=0, minute=0, second=0)
                    end_date = datetime.now().replace(hour=23, minute=59, second=59)
                    context = {'uuid': uuid, 'start_date': start_date, 'end_date': end_date}
                    
                    return render(request, "citizens/citizens-report.html", context)
                else:
                    citizen_register = CitizenRegister.objects.get(uuid=uuid)
                    # Get date range from one month ago today (trunc dates)
                    start_date = (datetime.now() - timedelta(days=30)).replace(hour=0, minute=0, second=0)
                    end_date = datetime.now().replace(hour=23, minute=59, second=59)
                    context = {'uuid': uuid, 'start_date': start_date, 'end_date': end_date}
                    return render(request, "citizens/citizens-report.html", context)
            else:
                return redirect("citizens-signup")

    except Exception as e:
        print (show_exc(e))
        return redirect("pwa-login")
    
def citizens_signup (request):
    towns = []
    form = None
    uuid = None
    try:
        towns = Town.objects.all().order_by("island__name", "name")
        if request.method == "POST":
            uuid = request.POST.get("uuid", None)
            if CitizenRegister.objects.filter(uuid=uuid).exists():
                instance = CitizenRegister.objects.get(uuid=uuid)
            else:
                instance = CitizenRegister(uuid=uuid)
            form = CitizenRegisterForm(request.POST, instance=instance)
            if form.is_valid():
                citizen_register = form.save()

                return render(request, "citizens/citizens-email-sent.html", {'error':send_email(citizen_register)})
            else:
                print (form.errors)
                return render (request, "citizens/citizens-signup.html", {'form': form, 'towns': towns, 'uuid': uuid})
        else:
            import uuid
            uuid = str(uuid.uuid4())
            form = CitizenRegisterForm(instance=CitizenRegister(uuid=uuid))
            return render (request, "citizens/citizens-signup.html", {'form': form, 'towns': towns, 'uuid': uuid})

    except Exception as e:
        print (show_exc(e))
        return render (request, "citizens/citizens-signup.html", {'form': form, 'towns': towns, 'uuid': uuid})

def send_email(citizen):
    try:
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        email_html = render_to_string("citizens/citizens-email.html", {'uuid': citizen.uuid})
        send_mail("Plataforma de Gestión de residuos de Gesplan", "emailtest@shidix.com", [citizen_register.email], html_message=email_html, fail_silently=False)
    except Exception as e:
        print (show_exc(e))
        return False
    return True

    
def citizens_login(request):
    try:
        if request.method == "POST":
            dni = request.POST.get("dni", None)
            control_key = request.POST.get("control_key", None)
            if control_key == "SZRf2QMpIfZHPEh0ib7YoDlnnDp5HtjDqbAw":
                if CitizenRegister.objects.filter(identification=dni).exists():
                    citizen_register = CitizenRegister.objects.get(identification=dni)
                    return render(request, "citizens/citizens-email-sent", {'error':send_email(citizen_register)})
                else:
                    return redirect("citizens-signup")
            else:
                return redirect("citizens-login")
        else:
            import uuid
            uuid = str(uuid.uuid4())
        return render(request, "citizens/citizens-login.html")
    except Exception as e:
        print (show_exc(e))
        return redirect("citizens-login")

def citizens_logout(request):
    return redirect("pwa-login")

def citizens_check_certificate(request, uuid=None):
    if uuid is None:
        return HttpResponse("Certificado no validado")
    
    uuid = request.POST.get("uuid", None)
    if CitizenRegister.objects.filter(uuid=uuid).exists():
        citizen_register = CitizenRegister.objects.get(uuid=uuid)
        return render(request, "citizens/citizens-check-cert.html", {'error': False})
    else:
        return render(request, "citizens/citizens-check-cert.html", {'error': True})
