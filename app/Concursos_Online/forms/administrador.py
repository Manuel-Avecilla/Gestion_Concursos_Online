# ============================================================
# region Importaciones
# ============================================================

from django import forms
from django.forms import ModelForm
from Concursos_Online.models import Administrador

# endregion
# ============================================================




# ============================================================
# region Formulario Modelo
# ============================================================

class AdministradorForm(ModelForm):

    class Meta:
        model = Administrador
        fields = ["usuario", "area_responsable", "activo", "horario_disponible"]
        labels = {
            "usuario": "Usuario asociado",
            "area_responsable": "Área responsable",
            "activo": "¿Activo?",
            "horario_disponible": "Horario disponible",
        }
        help_texts = {
            "area_responsable": "Máximo 100 caracteres.",
            "horario_disponible": "Hora en formato HH:MM (opcional).",
        }
        widgets = {
            "horario_disponible": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }

    def clean(self):
        # Validamos con el modelo actual
        cleaned_data = super().clean()

        #Obtenemos los campos 
        area_responsable = cleaned_data.get('area_responsable')
        activo = cleaned_data.get('activo')
        horario_disponible = cleaned_data.get('horario_disponible')

        #Comprobamos
        if not activo and horario_disponible:
            self.add_error("horario_disponible","No puede asignar horario disponible si el administrador no está activo.")

        if area_responsable and len(area_responsable) < 3:
            self.add_error("area_responsable","El área responsable debe tener al menos 3 caracteres.")

        #Siempre devolvemos el conjunto de datos.
        return cleaned_data

# endregion
# ============================================================




# ============================================================
# region Formulario Busqueda Avanzada
# ============================================================

class AdministradorBuscarAvanzada(forms.Form):

    area_contiene = forms.CharField(
        label='Área responsable contiene',
        help_text="(Opcional)",
        required=False
    )

    activo = forms.ChoiceField(
        label='Estado',
        help_text="(Opcional)",
        required=False,
        choices=[
            ("-", "Cualquiera"),
            ("1", "Activo"),
            ("0", "Inactivo"),
        ],
        initial="-",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "style": "max-width: 200px;",
            }
        ),
    )

    horario_minimo = forms.TimeField(
        label="Horario después de",
        required=False,
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
                "style": "max-width: 170px;",
            }
        )
    )

    horario_maximo = forms.TimeField(
        label="Horario antes de",
        required=False,
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
                "style": "max-width: 170px;",
            }
        )
    )

    def clean(self):
        
        super().clean()

        #Obtenemos los campos
        area_contiene = self.cleaned_data.get('area_contiene')
        activo = self.cleaned_data.get('activo')
        horario_minimo = self.cleaned_data.get('horario_minimo')
        horario_maximo = self.cleaned_data.get('horario_maximo')

        #Comprobamos
        if(
            area_contiene == "" and
            activo is None and
            horario_minimo is None and
            horario_maximo is None
        ):
            self.add_error('area_contiene', 'Debes rellenar al menos un campo.')
            self.add_error('activo', 'Debes rellenar al menos un campo.')
            self.add_error('horario_minimo', 'Debes rellenar al menos un campo.')
            self.add_error('horario_maximo', 'Debes rellenar al menos un campo.')
            
        
        if area_contiene and len(area_contiene.strip()) > 100:
            self.add_error('area_contiene', 'El área responsable no puede tener más de 100 caracteres.')

        if horario_minimo and horario_maximo:
            if horario_minimo >= horario_maximo:
                self.add_error('horario_maximo', 'Debe ser una hora posterior al campo "Horario después de".')

        if activo not in ("-", "1", "0"):
            self.add_error("activo", "Valor inválido para el campo de estado.")

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================
