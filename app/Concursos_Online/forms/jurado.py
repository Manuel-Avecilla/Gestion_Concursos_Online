# ============================================================
# region Importaciones
# ============================================================

from django import forms
from django.forms import ModelForm
from Concursos_Online.models import Jurado

# endregion
# ============================================================




# ============================================================
# region Formulario Modelo
# ============================================================

class JuradoForm(ModelForm):

    class Meta:
        model = Jurado
        fields = ["usuario", "experiencia", "especialidad", "disponible", "puntuacion_media","concursos"]
        labels = {
            "usuario": ("Usuario asociado"),
            "experiencia": ("Años de experiencia"),
            "especialidad": ("Especialidad"),
            "disponible": ("¿Disponible?"),
            "puntuacion_media": ("Puntuación media"),
            "concursos": ("Concursos Asignados")
        }
        help_texts = {
            "experiencia": ("Debe ser un número positivo."),
            "especialidad": ("100 caracteres como máximo."),
            "puntuacion_media": ("Valor decimal entre 0 y 999.99"),
            "concursos": ("Para selecionar los elementos manten pulsada la tecla Ctrl"),
        }
        widgets = {
            "concursos": forms.SelectMultiple(
                attrs={
                'class': 'form-select',
                'size': '6'
                }
            ),
        }

    def clean(self):
        # Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        experiencia = self.cleaned_data.get('experiencia')
        especialidad = self.cleaned_data.get('especialidad')
        puntuacion_media = self.cleaned_data.get('puntuacion_media')

        #Comprobamos
        if experiencia is not None and experiencia < 0:
            self.add_error('experiencia', 'La experiencia no puede ser negativa.')

        if especialidad and len(especialidad) < 3:
            self.add_error('especialidad', 'La especialidad debe tener al menos 3 caracteres.')

        if puntuacion_media is not None and (puntuacion_media < 0 or puntuacion_media > 999.99):
            self.add_error('puntuacion_media', 'La puntuación debe estar entre 0 y 999.99.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================




# ============================================================
# region Formulario Busqueda Avanzada
# ============================================================

class JuradoBuscarAvanzada(forms.Form):
    
    usuario_contiene = forms.CharField(
        label='Nombre de usuario contiene',
        help_text="(Opcional)",
        required=False
    )

    especialidad_contiene = forms.CharField(
        label='Especialidad contiene',
        help_text="(Opcional)",
        required=False
    )
    
    experiencia_minima = forms.IntegerField(
        label='Experiencia mínima (años)',
        help_text="(Opcional)",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 170px;",
                "min": 0, 
                "max": 80,
                "step": 1,
            }
        ),
    )

    puntuacion_minima = forms.DecimalField(
        label='Puntuación mínima',
        required=False,
        initial=0,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "class": "form-range",
                "min": 0, 
                "max": 100,
                "step": 0.1,
            }
        ),
    )
    
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        usuario_contiene = self.cleaned_data.get('usuario_contiene')
        especialidad_contiene = self.cleaned_data.get('especialidad_contiene')
        experiencia_minima = self.cleaned_data.get('experiencia_minima')
        puntuacion_minima = self.cleaned_data.get('puntuacion_minima')
        
        #Comprobamos
        if usuario_contiene and len(usuario_contiene.strip()) > 50:
            self.add_error('usuario_contiene', 'El nombre de usuario no puede tener más de 50 caracteres.')

        if especialidad_contiene and len(especialidad_contiene.strip()) > 100:
            self.add_error('especialidad_contiene', 'La especialidad no puede tener más de 100 caracteres.')
        
        if experiencia_minima is not None and experiencia_minima < 0:
            self.add_error('experiencia_minima', 'La experiencia mínima debe ser 0 o superior.')

        if puntuacion_minima is not None and not (0 <= puntuacion_minima <= 100):
            self.add_error('puntuacion_minima', 'La puntuación debe estar entre 0 y 100.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================
