from django.contrib import admin

from .models import Usuario,Perfil,Participante,Administrador,Jurado,Notificacion,Recibe,Asigna,Concurso,Evaluacion,Inscribe,Trabajo

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Perfil)
admin.site.register(Participante)
admin.site.register(Administrador)
admin.site.register(Jurado)
admin.site.register(Notificacion)
admin.site.register(Recibe)
admin.site.register(Asigna)
admin.site.register(Concurso)
admin.site.register(Evaluacion)
admin.site.register(Inscribe)
admin.site.register(Trabajo)