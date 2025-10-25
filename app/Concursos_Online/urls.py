from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('concursos-online/listar', views.concursos_listar, name='lista_concursos'),
    path('concursos-online/<int:id_concurso>', views.dame_concurso, name='dame_concurso'),
    path('concursos-online/<int:anyo_concurso>/<int:mes_concurso>', views.dame_concursos_fecha, name='dame_concursos_fecha'),
    path('concursos-online/listar/activo/<str:activo>', views.dame_concurso_activo, name='dame_concurso_activo'),
    path('concursos-online/listar/texto/<str:texto>', views.dame_concurso_texto, name='dame_concurso_texto'),
]
