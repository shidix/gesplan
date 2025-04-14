# Formulario del modelo CitizenRegister
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Citizen, CitizenRegister, Town

class CitizenRegisterForm( ModelForm):
    """
    Formulario del modelo CitizenRegister
    """
    class Meta:
        model = CitizenRegister
        fields = ['first_name', 'last_name', 'identification', 'address', 'usual_plate', 'phone', 'email', 'uuid', 'town']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['town'].queryset = Town.objects.all()

