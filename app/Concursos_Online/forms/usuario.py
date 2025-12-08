# ============================================================
# region Importaciones
# ============================================================

from django import forms
from django.forms import ModelForm
from Concursos_Online.models import Usuario

# endregion
# ============================================================




# ============================================================
# region Formulario Modelo
# ============================================================

class UsuarioForm(ModelForm):

    class Meta:
        model = Usuario
        fields = ["username","email","password","rol"]
        labels = {
            "username":("Nombre de Usuario"),
            "correo":("Correo electrónico"),
            "password":("Contraseña"),
            "rol":("Rol"),
        }
        help_texts = {
            "username":("50 caracteres como máximo"),
        }

    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        #Comprobamos
        if len(username) < 3:
            self.add_error('username','El nombre debe tener al menos 3 caracteres.')
        
        if len(password) < 8:
            self.add_error('password','La contraseña debe tener al menos 8 caracteres.')

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================




# ============================================================
# region Formulario Busqueda Avanzada
# ============================================================

class UsuarioBuscarAvanzada(forms.Form):
    
    nombre_usuario_contiene = forms.CharField(
        label='Nombre de usuario contiene',
        help_text="(Opcional)",
        required=False
    )

    correo_contiene = forms.CharField(
        label='Correo contiene',
        help_text="(Opcional)",
        required=False
    )

    fecha_registro_desde = forms.DateField(
        label='Registro desde',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )

    fecha_registro_hasta = forms.DateField(
        label='Registro hasta',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )

    tipo_usuario = forms.ChoiceField(
        label='Tipo de usuario',
        help_text="Seleccione un tipo o 'Todos'",
        choices=[
            ('todos', 'Todos'),
            ('admin', 'Administrador'),
            ('jurado', 'Jurado'),
            ('participante', 'Participante'),
        ],
        required=True,
        initial='todos'
    )
    
    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()

        #Obtenemos los campos
        nombre_usuario_contiene = self.cleaned_data.get('nombre_usuario_contiene')
        correo_contiene = self.cleaned_data.get('correo_contiene')
        fecha_registro_desde = self.cleaned_data.get('fecha_registro_desde')
        fecha_registro_hasta = self.cleaned_data.get('fecha_registro_hasta')
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        
        #Comprobamos
        if(tipo_usuario == ""):
            self.add_error('tipo_usuario','Seleccione un tipo de Usuario.')
        
        if(
            not fecha_registro_desde is None and
            not fecha_registro_hasta is None and
            fecha_registro_hasta < fecha_registro_desde
            ):
            self.add_error('fecha_registro_desde','Rango de fecha no valido.')
            self.add_error('fecha_registro_hasta','Rango de fecha no valido.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================