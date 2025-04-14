#from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone as tz
from datetime import datetime

from gestion.models import Facility, Employee, Waste


class Island(models.Model):
    code = models.CharField(max_length=10, verbose_name=_('Código'), default='')
    name = models.CharField(max_length=200, verbose_name=_('Isla'))

    class Meta:
        verbose_name = _('Isla')
        verbose_name_plural = _('Islas')

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=200, verbose_name = _('Municipio'))
    island = models.ForeignKey(Island, verbose_name=_('Isla'), on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Municipio')
        verbose_name_plural = _('Municipios')

    def __str__(self):
        if self.island is not None:
            return "[%s] %s" % (self.island.code, self.name)
        else:
            return "[---] %s" % (self.name)

def get_next_code():
    try:
        c = Citizen.objects.all().order_by("-code").first()
        return str(int(c.code) + 1).zfill(6)
    except:
        return "000000"

class Citizen(models.Model):
    code = models.CharField(max_length=6, verbose_name=_('Código'), default=get_next_code, blank=True, null=True)
    device = models.CharField(max_length=255, verbose_name=_('Dispositivo'), null=True, blank=True)
    identification = models.CharField(max_length=200, verbose_name=_('Idenitificación'), null=False, blank=True, default="")
    address = models.CharField(max_length=255, verbose_name=_('Domicilio Social'), blank=True)
    plate = models.CharField(max_length=255, verbose_name=_('Matrícula'), blank=True)
    phone = models.CharField(max_length=12, null=True, default = '000000000', verbose_name = _('Teléfono'), blank=True)
    email = models.CharField(max_length=255, verbose_name=_('Correo eletrónico'), blank=True, default="")
    date = models.DateTimeField(verbose_name='Fecha y hora', default=tz.now)
    observations = models.TextField(verbose_name=_('Observaciones'), blank=True)

    town = models.ForeignKey(Town, verbose_name = _('Término municipal'), on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, verbose_name=_('Operario'), on_delete=models.SET_NULL, related_name="citizens", null=True, blank=True)
    facility = models.ForeignKey(Facility, verbose_name=_('Instalación'), on_delete=models.CASCADE, related_name="citizens")
    #citizen_user = models.ForeignKey('CitizenUser', verbose_name="CitizenUser", related_name="citizens", null=True, blank=True)

    def __str__(self):
        out = "[%s] - %s"%(self.facility, self.identification)
        #if self.citizen_user:
        #    out += " %s"%(self.citizen_user)
        return out

    def total_by_waste(self, waste, date_range = None):
        now = datetime.now()
        if date_range != None:
            idate = date_range[0].replace(hour=0, minute=0, second=0)
            edate = date_range[1].replace(hour=23, minute=59, second=59)
        else:
            idate = now.replace(hour=0, minute=0, second=0)
            edate = now.replace(hour=23, minute=59, second=59)
        units = WasteCitizen.objects.filter(citizen__plate=self.plate, waste=waste, citizen__date__range=(idate,edate)).aggregate(Sum('units'))["units__sum"]
        return 0 if units == None else units

    class Meta:
        verbose_name = _('Ciudadano')
        verbose_name_plural = _('Ciudadano')

class WasteCitizen(models.Model):
    units = models.FloatField(verbose_name=_('Cantidad'), blank=False, null=False)

    waste = models.ForeignKey(Waste, verbose_name = _('Residuo'), on_delete=models.SET_NULL, null=True)
    citizen = models.ForeignKey(Citizen, verbose_name=_('Ciudadano'), on_delete=models.CASCADE, null=True, related_name='wastes')

    class Meta:
        verbose_name = _('Residuo depositado')
        verbose_name = _('Residuos depositados')

    def __str__(self):
        return ("[%s] %s ha dejado %d de %s en la fecha %s" % (self.citizen.facility, self.citizen.identification, self.units, self.waste.name, self.citizen.date))
    
class CitizenRegister(models.Model):
    uuid = models.CharField(max_length=100, verbose_name=_('UUID'), default="", blank=True, unique=True)
    first_name = models.CharField(max_length=255, verbose_name=_('Nombre'), blank=True)
    last_name = models.CharField(max_length=255, verbose_name=_('Apellidos'), blank=True)
    usual_plate = models.CharField(max_length=255, verbose_name=_('Matrícula Habitual'), blank=True)
    address = models.CharField(max_length=255, verbose_name=_('Domicilio'), blank=True)
    identification = models.CharField(max_length=200, verbose_name=_('Identificación'), blank=True)
    phone = models.CharField(max_length=12, null=True, default = '000000000', verbose_name = _('Teléfono'), blank=True)
    email = models.CharField(max_length=255, verbose_name=_('Correo eletrónico'), blank=True)
    postcode = models.CharField(max_length=10, verbose_name=_('Código Postal'), blank=True)
    town = models.ForeignKey(Town, verbose_name=_('Municipio'), on_delete=models.SET_NULL, null=True, blank=True)
    signup_date = models.DateTimeField(verbose_name=_('Fecha de alta'), default=tz.now)
    verfied_date = models.DateTimeField(verbose_name=_('Fecha de verificación'), null=True, blank=True)


#    def save(self, *args, **kwargs):
#        super(WasteCitizen, self).save(*args, **kwargs)
#        if self.citizen.citizen_user != None:
#            calculate_score(self.citizen.citizen_user)

