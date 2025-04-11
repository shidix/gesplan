#from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone as tz
from datetime import datetime

from gestion.models import Facility, Employee, Waste


class ContractStatus(models.Model):
    code = models.CharField(max_length=10, verbose_name=_('Código'), default='')
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Estado del contrato')
        verbose_name_plural = _('Estados de los contratos')

class Contract(models.Model):
    #date = models.DateTimeField(verbose_name='Fecha y hora', default=tz.now, null=True, blank=True)
    number = models.IntegerField(verbose_name='Número', default=0, null=True, blank=True)
    status = models.ForeignKey(ContractStatus, verbose_name = _('Estado'), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _('Contrato')
        verbose_name_plural = _('Contratos')

class Epigraph(models.Model):
    code = models.CharField(max_length=10, verbose_name=_('Código'), default='')
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Epígrafe')
        verbose_name_plural = _('Epígrafes')

def upload_contract(instance, filename):
    ascii_filename = str(filename.encode('ascii', 'ignore'))
    instance.filename = ascii_filename
    #folder = "notes/%s" % (instance.id)
    folder = "contracts"
    return '/'.join(['%s' % (folder), datetime.now().strftime("%Y%m%d%H%M%S") + ascii_filename])

class ContractLot(models.Model):
    ini_date = models.DateTimeField(verbose_name='Fecha y hora', default=tz.now, null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='Fecha y hora', default=tz.now, null=True, blank=True)
    amount = models.FloatField(verbose_name='Presupuesto asignado', default=0, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))
    file = models.FileField(upload_to=upload_contract, blank=True, verbose_name="Fichero", help_text="Select file to upload")

    epigraph = models.ForeignKey(Epigraph, verbose_name = _('Epígrafe'), on_delete=models.SET_NULL, null=True, blank=True)
    contract = models.ForeignKey(Contract, verbose_name = _('Contrato'), on_delete=models.SET_NULL, null=True, blank=True, related_name="lots")

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _('Lote del Contrato')
        verbose_name_plural = _('Lotes de los Contratos')

def upload_invoice(instance, filename):
    ascii_filename = str(filename.encode('ascii', 'ignore'))
    instance.filename = ascii_filename
    #folder = "notes/%s" % (instance.id)
    folder = "invoices"
    return '/'.join(['%s' % (folder), datetime.now().strftime("%Y%m%d%H%M%S") + ascii_filename])

class Invoice(models.Model):
    date = models.DateTimeField(verbose_name='Fecha y hora', default=tz.now, null=True, blank=True)
    amount = models.FloatField(verbose_name='Importe', default=0, null=True, blank=True)
    company = models.CharField(max_length=255, verbose_name=_('Empresa'), null=True, blank=True, default="")
    concept = models.TextField(verbose_name=_('Observaciones'), blank=True, default="")
    file = models.FileField(upload_to=upload_invoice, blank=True, verbose_name="Fichero", help_text="Select file to upload")

    contract = models.ForeignKey(Contract, verbose_name = _('Contrato'), on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices")

    def __str__(self):
        return self.concept

    class Meta:
        verbose_name = _('Factura')
        verbose_name_plural = _('Facturas')


