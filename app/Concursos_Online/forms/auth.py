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
    
    alias = forms.CharField(max_length=50)
    edad = forms.IntegerField(min_value=0)

    class Meta(RegistroUsuarioForm.Meta):
        fields = RegistroUsuarioForm.Meta.fields + ('alias', 'edad')
# endregion

# region Formulario Registro Jurado
class RegistroJuradoForm(RegistroUsuarioForm):
    
    disponible = forms.BooleanField(initial=True)
    experiencia = forms.IntegerField(min_value=0)

    class Meta(RegistroUsuarioForm.Meta):
        fields = RegistroUsuarioForm.Meta.fields + ('disponible', 'experiencia')
# endregion

# endregion
# ============================================================




# ============================================================
# region Formulario Autentificacion
# ============================================================



# endregion
# ============================================================
