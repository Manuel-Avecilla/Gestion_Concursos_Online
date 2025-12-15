# ============================================================
# region Importaciones
# ============================================================

from django import forms
from Concursos_Online.models import Usuario
from django.contrib.auth.forms import UserCreationForm

# endregion
# ============================================================




# ============================================================
# region Formulario Registro
# ============================================================

# region Formulario Registro Usuario
class RegistroUsuarioForm(UserCreationForm):
    
    class Meta:
        model = Usuario
        fields = ('username','email','password1','password2')

    def clean_username(self):
        
        username = self.cleaned_data.get("username")

        # Si se esta editando un usuario → ignorar validacion contra si mismo
        if self.instance and self.instance.pk:
            existe = Usuario.objects.exclude(pk=self.instance.pk).filter(username=username).exists()
        
        else:
            existe = Usuario.objects.filter(username=username).exists()

        if existe:
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")

        return username
# endregion

# region Formulario Registro Participante
class RegistroParticipanteForm(RegistroUsuarioForm):
    
    alias = forms.CharField(
        max_length=50,
        label="Tu Alias como Participante"
    )
    edad = forms.IntegerField(
        min_value=0,
        label="¿Cuantos años tienes?"
    )

    class Meta(RegistroUsuarioForm.Meta):
        fields = RegistroUsuarioForm.Meta.fields + ('alias', 'edad')
    
    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()
        
        # Obtener datos
        alias = self.cleaned_data.get('alias')
        edad = self.cleaned_data.get('edad')

        #Comprobamos
        if(alias == "" and edad is None):
            self.add_error("alias", "Debes rellenar al menos un campo.")
            self.add_error("edad", "Debes rellenar al menos un campo.")

        if len(alias) < 3:
            self.add_error("alias", "El alias debe tener al menos 3 caracteres.")
        
        if edad < 10:
            self.add_error("edad", "Debes tener al menos 10 años para poder ser Participante")

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
# endregion

# region Formulario Registro Jurado
class RegistroJuradoForm(RegistroUsuarioForm):
    
    especialidad = forms.CharField(
        max_length=50,
        label="Especialidad como Jurado"
    )
    experiencia = forms.IntegerField(
        min_value=0,
        label="Años de Experiencia"
    )

    class Meta(RegistroUsuarioForm.Meta):
        fields = RegistroUsuarioForm.Meta.fields + ('especialidad', 'experiencia')
    
    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()
        
        # Obtener datos
        especialidad = self.cleaned_data.get('especialidad')
        experiencia = self.cleaned_data.get('experiencia')

        #Comprobamos
        if(especialidad == "" and experiencia is None):
            self.add_error("especialidad", "Debes rellenar al menos un campo.")
            self.add_error("experiencia", "Debes rellenar al menos un campo.")

        if len(especialidad) < 3:
            self.add_error("especialidad", "La especialidad debe tener al menos 3 caracteres.")
        
        if experiencia > 60:
            self.add_error("experiencia", "La experiencia no puede ser superior a 60 años")

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
# endregion

# endregion
# ============================================================




# ============================================================
# region Formulario Autentificacion
# ============================================================



# endregion
# ============================================================
