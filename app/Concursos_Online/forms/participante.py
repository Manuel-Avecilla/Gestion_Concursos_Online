# ============================================================
# region Importaciones
# ============================================================

from django import forms
from django.forms import ModelForm
from Concursos_Online.models import Participante

# endregion
# ============================================================




# ============================================================
# region Formulario Modelo
# ============================================================

class ParticipanteForm(ModelForm):
    
    class Meta:
        model = Participante
        fields = ["usuario","alias","edad","nivel","puntuacion_total"]
        labels = {
            "usuario":("Usuario"),
            "alias":("Alias"),
            "edad":("Edad"),
            "nivel":("Nivel"),
            "puntuacion_total":("Puntuacion Total"),
        }
        help_texts = {
            "alias":("20 caracteres como máximo"),
            "edad":("Solo mayores de 10 años"),
        }
        widgets = {
            "edad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 110px;",
                    "min": 1,
                    "max": 100,
                    "step": 1,
                }
            ),
            "nivel": forms.NumberInput(
                attrs={
                    "type": "range",
                    "class": "form-range",
                    "min": 1, 
                    "max": 5,
                }
            ),
            "puntuacion_total": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 110px;",
                    "min": 1,
                    "max": 100,
                    "step": 0.01,
                }
            )
        }

    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        alias = self.cleaned_data.get('alias')
        edad = self.cleaned_data.get('edad')
        nivel = self.cleaned_data.get('nivel')
        puntuacion_total = self.cleaned_data.get('puntuacion_total')

        #Comprobamos
        if len(alias) > 20:
            self.add_error('alias','El alias debe tener menos de 20 caracteres.')
        
        if edad < 10:
            self.add_error('edad','Solo mayores de 10 años')
            
        if edad > 100:
            self.add_error('edad','Edad Incorrecta')
        
        if puntuacion_total < 0 or puntuacion_total > 100:
            self.add_error('puntuacion_total','Puntuacion Total Incorrecta')
        
        if nivel < 0 or nivel > 5:
            self.add_error('nivel','Nivel Incorrecto')

        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================




# ============================================================
# region Formulario Busqueda Avanzada
# ============================================================

class ParticipanteBuscarAvanzada(forms.Form):
    
    alias_contiene = forms.CharField(
        label='Alias contiene',
        help_text="(Opcional)",
        required=False
    )
    
    edad_minima = forms.IntegerField(
        label='Edad minima',
        help_text="(Opcional)",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 170px;",
                "min": 1, 
                "max": 100,
                "step": 1,
            }
        ),
    )

    nivel_minimo = forms.IntegerField(
        label='Nivel minimo',
        required=False,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "class": "form-range",
                "min": 1, 
                "max": 5,
            }
        ),
    )
    
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        alias_contiene = self.cleaned_data.get('alias_contiene')
        edad_minima = self.cleaned_data.get('edad_minima')
        nivel_minimo = self.cleaned_data.get('nivel_minimo')
        
        #Comprobamos
        if alias_contiene and len(alias_contiene.strip()) > 20:
            self.add_error('alias_contiene', 'El alias no puede tener más de 20 caracteres')
        
        if edad_minima is not None and not (10 <= edad_minima <= 100):
            self.add_error('edad_minima', 'La edad debe estar entre 10 y 100.')

        if nivel_minimo is not None and not (1 <= nivel_minimo <= 5):
            self.add_error('nivel_minimo', 'El nivel debe estar entre 1 y 5.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================
