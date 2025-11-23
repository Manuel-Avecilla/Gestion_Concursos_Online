from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('',views.home, name='home'),
    path('menu',views.menu, name='menu'),
    path('concursos-online/listar', views.concursos_listar, name='lista_concursos'),
    path('concursos-online/<int:id_concurso>', views.dame_concurso, name='dame_concurso'),
    path('concursos-online/<int:anyo_concurso>/<int:mes_concurso>', views.dame_concursos_fecha, name='dame_concursos_fecha'),
    path('concursos-online/listar/activo/<str:activo>', views.dame_concurso_activo, name='dame_concurso_activo'),
    path('concursos-online/listar/texto/<str:texto>', views.dame_concurso_texto, name='dame_concurso_texto'),
    path('concursos-online/ultimo-participante-inscrito/<int:id_concurso>', views.dame_ultimo_participante, name='dame_ultimo_participante'),
    re_path(r'^participante/(?P<alias_participante>[a-zA-Z0-9_-]+)/$', views.detalle_participante_alias, name='detalle_participante_alias'),
    path('usuarios_sin_notificaciones/', views.usuarios_sin_notificar, name='usuarios_sin_notificar'),
    path('jurados/listar', views.dame_jurados, name='dame_jurados'),
    path('jurados/metricas_experiencia/', views.metricas_experiencia_jurados, name='metricas_experiencia_jurados'),
    
    path('participantes',views.participantes_listar, name='participantes_listar'),
    path('usuario/<int:id_usuario>', views.dame_usuario, name='dame_usuario'),
    path('jurado/<int:id_jurado>', views.dame_jurado, name='dame_jurado'),
    path('participantes/concurso/<int:id_concurso>',views.dame_participantes_concurso, name='dame_participantes_concurso'),
    
    #--------------CRUD--------------
    #---Usuario---
    path('usuario/crear/',views.usuario_create, name='usuario_create'),
    path('usuario/buscar/',views.usuario_buscar, name='usuario_buscar'),
    
]

# Explicacion re_path:
# Patrón: ^participante/CUALQUIER_CADENA/$.
# ?P<alias_participante> Esto nombra la parte capturada como alias_participante
# Si un usuario navega a http://127.0.0.1:8000/participante/usuario_ejemplo123/
# la cadena usuario_ejemplo123 será capturada como la variable alias_participante y pasada a la vista.