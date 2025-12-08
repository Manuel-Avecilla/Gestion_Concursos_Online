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

class RegistroForm(UserCreationForm):
    
    roles = (
        (Usuario.PARTICIPANTE, 'Participante'),
        (Usuario.JURADO, 'Jurado'),
    )
    rol = forms.ChoiceField(choices=roles)
    
    class Meta:
        model = Usuario
        fields = ('username','email','password1','password2','rol')

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
# ============================================================




# ============================================================
# region Formulario Autentificacion
# ============================================================



# endregion
# ============================================================
