from django import forms
from django.forms import ModelForm
from .models import *

from datetime import date #Para conseguir el año actual
from django.core.files.uploadedfile import UploadedFile

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
#----------------------------------------------------------------------------

#----------------------------------PERFIL-----------------------------------
class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ["usuario","nombre_completo","biografia","fecha_nacimiento","imagen_perfil"]
        labels = {
            "usuario":("Usuario"),
            "nombre_completo":("Nombre Completo"),
            "biografia":("Biografia"),
            "fecha_nacimiento":("Fecha de nacimiento"),
            "imagen_perfil":("Foto de perfil"),
        }
        help_texts = {
            "nombre_completo":("50 caracteres como máximo"),
            "biografia":("100 caracteres como máximo")
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type':'date'},format='%Y-%m-%d'),
            'imagen_perfil': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),
        }

    def clean(self):
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre_completo = self.cleaned_data.get('nombre_completo')
        biografia = self.cleaned_data.get('biografia')
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        imagen = self.cleaned_data.get("imagen_perfil")

        #Comprobamos
        if nombre_completo and len(nombre_completo) < 5:
            self.add_error("nombre_completo", "El nombre debe tener al menos 5 caracteres.")

        if biografia and len(biografia) < 10:
            self.add_error("biografia", "La biografia debe tener al menos 10 caracteres.")

        if fecha_nacimiento is None:
            self.add_error("fecha_nacimiento", "Debes introducir una fecha.")
        elif fecha_nacimiento > date.today():
            self.add_error("fecha_nacimiento", "La fecha no puede ser superior a hoy.")

        # Validacion de imagen
        if imagen and isinstance(imagen, UploadedFile):
            # Tamaño maximo 2MB
            if imagen.size > 2 * 1024 * 1024:
                self.add_error("imagen_perfil", "La imagen no debe superar 2MB.")

            # Formatos permitidos
            ext = imagen.name.lower()
            if not ext.endswith((".png", ".jpg", ".jpeg", ".webp")):
                self.add_error("imagen_perfil", "Formato no valido. Usa PNG, JPG o WEBP.")
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class PerfilBuscarAvanzada(forms.Form):
    
    biografia_contiene = forms.CharField(
        label='Biografia contiene',
        help_text="(Opcional)",
        required=False
    )
    
    fecha_nacimiento_desde = forms.DateField(
        label='Fecha Nacimiento desde',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )

    fecha_nacimiento_hasta = forms.DateField(
        label='Fecha Nacimiento hasta',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type':'date'})
    )
    
    usuarios = forms.ModelMultipleChoiceField(
        label='Ver perfiles de usuarios',
        help_text="(Opcional). Para selecionar los elementos manten pulsada la tecla Ctrl",
        queryset=Usuario.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': '9'
        })
    )
    
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        biografia_contiene = self.cleaned_data.get('biografia_contiene')
        fecha_nacimiento_desde = self.cleaned_data.get('fecha_nacimiento_desde')
        fecha_nacimiento_hasta = self.cleaned_data.get('fecha_nacimiento_hasta')
        usuarios = self.cleaned_data.get('usuarios')
        
        #Comprobamos
        
        if (
            biografia_contiene == "" and
            fecha_nacimiento_desde is None and
            fecha_nacimiento_hasta is None and
            len(usuarios) == 0
        ):
            self.add_error('biografia_contiene','Debes rellenar al menos un campo.')
            self.add_error('fecha_nacimiento_desde','Debes rellenar al menos un campo.')
            self.add_error('fecha_nacimiento_hasta','Debes rellenar al menos un campo.')
            self.add_error('usuarios','Debes rellenar al menos un campo.')
        
        if(
            not fecha_nacimiento_desde is None and
            not fecha_nacimiento_hasta is None and
            fecha_nacimiento_hasta < fecha_nacimiento_desde
            ):
            self.add_error('fecha_nacimiento_desde','Rango de fecha no valido.')
            self.add_error('fecha_nacimiento_hasta','Rango de fecha no valido.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
#----------------------------------------------------------------------------

#----------------------------------PARTICIPANTE------------------------------
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
#----------------------------------------------------------------------------

#----------------------------------ADMINISTRADOR-----------------------------
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
#----------------------------------------------------------------------------

#----------------------------------JURADO------------------------------------
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
#----------------------------------------------------------------------------