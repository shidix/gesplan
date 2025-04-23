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
        fields = ['first_name', 'last_name', 'identification', 'address', 'usual_plate', 'phone', 'email', 'uuid', 'town', 'postcode']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['town'].queryset = Town.objects.all()

    def clean_identification(self):
        """
        Validación del campo identification
        """
        identification = self.cleaned_data.get('identification')
        if not identification:
            raise ValidationError(_('Este campo es obligatorio'))
        if not identification.isalnum():
            raise ValidationError(_('El campo DNI solo puede contener letras y números'))
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        if len(identification) != 9:
            raise ValidationError(_('El DNI debe tener 9 caracteres'))
        
        numeros = identification[:-1]
        letra = identification[-1].upper()
        
        if not numeros.isdigit():
            raise ValidationError(_('El campo DNI debe cumplir el formato correcto'))
        
        numero = int(numeros)
        letra_correcta = letras[numero % 23]
        
        if letra != letra_correcta:
            raise ValidationError(_('La letra de la identificación no es correcta'))
    
        return identification
    
    def clean_postcode(self):
        """
        Validación del campo postcode
        """
        postcode = self.cleaned_data.get('postcode')
        if not postcode:
            raise ValidationError(_('Este campo es obligatorio'))
        if not postcode.isdigit():
            raise ValidationError(_('El campo código postal solo puede contener números'))
        if len(postcode) != 5:
            raise ValidationError(_('El código postal debe tener 5 dígitos'))
        if not (38000 <= int(postcode) <= 38999):
            raise ValidationError(_('El código postal no es válido'))
        
        return postcode
    
    def clean_email(self):
        """
        Validación del campo email
        """
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError(_('Este campo es obligatorio'))
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise ValidationError(_('El correo electrónico no es válido'))
        
        return email