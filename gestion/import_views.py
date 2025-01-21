from django.http import HttpResponse
from django.shortcuts import render, redirect

from gesplan.decorators import group_required
from gesplan.commons import get_int, get_float, get_or_none, get_param, get_session, set_session, show_exc
from .models import *

def clean(val):
    return val.rstrip().lstrip()

@group_required("admins",)
def import_db(request):
    return render(request, "import/import.html")

@group_required("admins",)
def import_db_file(request):
    try:
        f = request.FILES["file"]
        db = request.POST["db"]

        lines = f.read().decode('latin-1').splitlines()
        for line in lines:
            #print(line)
            l = line.split("|")
            #print(l[1])
            if db == "comp":
                Company.objects.get_or_create(ext_code=clean(l[0]), name=clean(l[1]), register_number=get_int(clean(l[6])), nif=clean(l[3]), phone=clean(l[4]), email=clean(l[5]), address=clean(l[7]), cp=clean(l[8]), town=clean(l[10]), province=clean(l[9]))
            elif db == "fac":
                comp = get_or_none(Company, l[5].strip(), "ext_code")
                comp_own = get_or_none(Company, l[11].strip(), "ext_code")

                Facility.objects.get_or_create(ext_code=clean(l[0]), code=clean(l[2]), nima=clean(l[8]), description=clean(l[3]), address=clean(l[10]), town=clean(l[12]), company=comp, company_owner=comp_own)
            elif db == "trucktype":
                TruckType.objects.get_or_create(ext_code=clean(l[0]), brand=clean(l[1]), model=clean(l[2]), year=clean(l[3]))
            elif db == "truck":
                av = True if clean(l[3]) == "t" else False
                sat = True if clean(l[8]) == "t" else False
                date = datetime.datetime.strptime(clean(l[9]), "%Y-%m-%d")
                
                tt = get_or_none(TruckType, l[6].strip(), "ext_code")
                comp = get_or_none(Company, l[7].strip(), "ext_code")

                Truck.objects.get_or_create(ext_code=clean(l[0]), available=av, on_saturday=sat, itv_date=date, number_plate=clean(l[2]), observations=clean(l[5]), type=tt, company=comp)
            elif db == "employee":
                ac = True if clean(l[12]) == "t" else False
                name = "{} {}".format(clean(l[3]), clean(l[4]))

                fac = get_or_none(Facility, l[9].strip(), "ext_code")
                comp = get_or_none(Company, l[7].strip(), "ext_code")

                Employee.objects.get_or_create(ext_code=clean(l[0]), active=ac, code=clean(l[1]), nif=clean(l[2]), pin=clean(l[10]), device_uid=clean(l[11]), name=name, cellphone=clean(l[5]), email=clean(l[6]), company=comp, facility=fac)
            elif db == "waste":
                dangerous = True if clean(l[4]) == "t" else False
                alert = True if clean(l[7]) == "t" else False

                units = get_or_none(UnitType, l[5].strip())
                comp = get_or_none(Company, l[10].strip(), "ext_code")

                Waste.objects.get_or_create(ext_code=clean(l[0]), alert=alert, dangerous=dangerous, ler=get_int(clean(l[8])), day_limit=get_float(clean(l[9])), score=get_float(clean(l[13])), code=clean(l[1]), name=clean(l[2]), description=clean(l[3]), recycle_text=clean(l[12]), units=units, external_manager=comp)
            elif db == "wasteinfacility":
                toRoute= True if clean(l[4]) == "t" else False
                date = clean(l[10])
                if "+" in date:
                    date = date.split("+")[0]
                if "." in date:
                    date = date.split(".")[0]
                last_modification = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

                waste = get_or_none(Waste, l[4].strip(), "ext_code")
                fac = get_or_none(Facility, l[3].strip(), "ext_code")

                WasteInFacility.objects.get_or_create(ext_code=clean(l[0]), toRoute=toRoute, code=clean(l[6]), filling_degree=get_float(l[1]), warning_filling_degree=get_float(l[5]), alert_filling_degree=get_float(l[2]), last_modification=last_modification, advise_frec=15, emails="", subject="", body="", waste=waste, facility=fac)
 
        return redirect("import")
    except Exception as e:
        return render(request, 'error_exception.html', {'exc':show_exc(e)})

    return render(request, "import.html")
