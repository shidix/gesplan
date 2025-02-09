#from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone as tz

from gestion.models import Facility, Employee


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

    class Meta:
        verbose_name = _('Ciudadano')
        verbose_name_plural = _('Ciudadano')

