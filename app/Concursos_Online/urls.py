from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('',views.index, name='index'),
    path('concursos-online/listar', views.concursos_listar, name='lista_concursos'),
    path('concursos-online/<int:id_concurso>', views.dame_concurso, name='dame_concurso'),
    path('concursos-online/<int:anyo_concurso>/<int:mes_concurso>', views.dame_concursos_fecha, name='dame_concursos_fecha'),
    path('concursos-online/listar/activo/<str:activo>', views.dame_concurso_activo, name='dame_concurso_activo'),
    path('concursos-online/listar/texto/<str:texto>', views.dame_concurso_texto, name='dame_concurso_texto'),
    path('concursos-online/ultimo-participante-inscrito/<int:id_concurso>', views.dame_ultimo_participante, name='dame_ultimo_participante'),
    re_path(r'^participante/(?P<alias_participante>[a-zA-Z0-9_-]+)/$', views.detalle_participante_alias, name='detalle_participante_alias'),
    path('usuarios_sin_notificaciones/', views.usuarios_sin_notificar, name='usuarios_sin_notificar'),
]

# Explicacion re_path:
# Patrón: ^participante/CUALQUIER_CADENA/$.
# ?P<alias_participante> Esto nombra la parte capturada como alias_participante
# Si un usuario navega a http://127.0.0.1:8000/participante/usuario_ejemplo123/
# la cadena usuario_ejemplo123 será capturada como la variable alias_participante y pasada a la vista.