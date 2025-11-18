from django import forms
from django.forms import ModelForm
from .models import *


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