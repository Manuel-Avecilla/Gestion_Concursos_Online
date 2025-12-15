# ============================================================
# region Importaciones
# ============================================================

from django import forms
from django.forms import ModelForm
from Concursos_Online.models import Concurso

# endregion
# ============================================================




# ============================================================
# region Formulario Modelo
# ============================================================

class ConcursoForm(ModelForm):

    class Meta:
        model = Concurso
        fields = [
            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_final",
            "activo",
            "ganador",
            "participantes",
        ]

        labels = {
            "nombre": "Nombre del concurso",
            "descripcion": "Descripción",
            "fecha_inicio": "Fecha de inicio",
            "fecha_final": "Fecha de finalización",
            "activo": "¿Activo?",
            "ganador": "Ganador",
            "participantes": "Participantes del concurso",
        }

        help_texts = {
            "nombre": "Máximo 100 caracteres.",
            "descripcion": "Describe brevemente el concurso.",
            "fecha_inicio": "Debe ser una fecha válida.",
            "ganador": "(Opcional)",
            "fecha_final": "Debe ser posterior a la fecha de inicio.",
        }

        widgets = {
            "fecha_inicio": forms.DateTimeInput(attrs={"type": "datetime-local"},format='%Y-%m-%dT%H:%M'),
            "fecha_final": forms.DateTimeInput(attrs={"type": "datetime-local"},format='%Y-%m-%dT%H:%M'),
            "participantes": forms.SelectMultiple(
                attrs={
                'class': 'form-select',
                'size': '6'
                }
            ),
        }

    def clean(self):

        super().clean()

        # Obtener datos
        nombre = self.cleaned_data.get('nombre')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_final = self.cleaned_data.get('fecha_final')

        # --- Validaciones personalizadas ---

        if nombre and len(nombre) < 3:
            self.add_error("nombre", "El nombre debe tener al menos 3 caracteres.")

        if fecha_inicio and fecha_final:
            if fecha_final < fecha_inicio:
                self.add_error(
                    "fecha_final",
                    "La fecha de finalización debe ser posterior a la fecha de inicio."
                )

        return self.cleaned_data

# endregion
# ============================================================




# ============================================================
# region Formulario Busqueda Avanzada
# ============================================================

class ConcursoBuscarAvanzada(forms.Form):
    
    nombre_contiene = forms.CharField(
        label='Nombre contiene',
        help_text="(Opcional)",
        required=False
    )
    
    fecha_inicio_minima = forms.DateTimeField(
        label='Fecha de inicio después de',
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
                "style": "max-width: 250px;"
            }
        )
    )

    fecha_final_maxima = forms.DateTimeField(
        label='Fecha de finalización antes de',
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
                "style": "max-width: 250px;"
            }
        )
    )

    activo = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[
            ("", "Cualquiera"),
            ("1", "Solo activos"),
            ("0", "Solo inactivos"),
        ],
        widget=forms.Select(attrs={"class": "form-select"})
    )
    
    def clean(self):
        
        super().clean()
        
        # Obtenemos los campos
        nombre_contiene = self.cleaned_data.get('nombre_contiene')
        fecha_inicio_minima = self.cleaned_data.get('fecha_inicio_minima')
        fecha_final_maxima = self.cleaned_data.get('fecha_final_maxima')
        activo = self.cleaned_data.get('activo')

        #Comprobamos
        if nombre_contiene and len(nombre_contiene.strip()) > 100:
            self.add_error('nombre_contiene', 'El nombre no puede tener más de 100 caracteres.')

        if fecha_inicio_minima and fecha_final_maxima:
            if fecha_final_maxima < fecha_inicio_minima:
                self.add_error(
                    'fecha_final_maxima',
                    'La fecha final debe ser posterior a la fecha inicial.'
                )

        if activo not in ["", "1", "0"]:
            self.add_error('activo', 'Valor no reconocido.')

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================
