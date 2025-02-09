from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone as tz

from django.contrib.auth.models import User
import datetime


class IncidentType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Código'))
    operator = models.BooleanField(default=False, verbose_name = _('Operario'))
    driver = models.BooleanField(default=False, verbose_name = _('Conductor'))

    class Meta:
        verbose_name = _('Tipo de Incidente')
        verbose_name_plural = _('Tipos de Incidentes')

    def __str__(self):
        return self.name

class Incident(models.Model):
    closed = models.BooleanField(default=False, verbose_name = _('Estado'))
    code = models.CharField(max_length=10, verbose_name=_('Código'))
    subject = models.CharField(max_length=255, verbose_name=_('Asunto'))
    description = models.TextField(verbose_name=_('Descripción'), default='', blank=True, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name=_('Creado el'))
    closed_date = models.DateTimeField(default=datetime.datetime.max, blank=True, null=True, verbose_name=_('Cerrado el'))

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('Creada por'))
    type = models.ForeignKey(IncidentType, on_delete=models.SET_NULL, verbose_name=_('Tipo'), blank=False, null=True, related_name='incidents')

    class Meta:
        verbose_name = _('Incidente')
        verbose_name_plural = _('Incidentes')
        ordering = ['-creation_date']

    def __str__(self):
        return self.subject

