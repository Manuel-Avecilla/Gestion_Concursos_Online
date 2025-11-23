from django import forms
from django.forms import ModelForm
from .models import *

#----------------------------------USUARIO-----------------------------------
class UsuarioForm(ModelForm):

    class Meta:
        model = Usuario
        fields = ["nombre_usuario","correo","password"]
        labels = {
            "nombre_usuario":("Nombre de Usuario"),
            "correo":("Correo electrónico"),
            "password":("Contraseña"),
        }
        help_texts = {
            "nombre_usuario":("50 caracteres como máximo"),
        }

    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre_usuario = self.cleaned_data.get('nombre_usuario')
        password = self.cleaned_data.get('password')

        #Comprobamos
        if len(nombre_usuario) < 3:
            self.add_error('nombre_usuario','El nombre debe tener al menos 3 caracteres.')
        
        if len(password) < 8:
            self.add_error('password','La contraseña debe tener al menos 8 caracteres.')

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class UsuarioBuscar(forms.Form):
    textoBusqueda = forms.CharField(required=True)

#----------------------------------------------------------------------------