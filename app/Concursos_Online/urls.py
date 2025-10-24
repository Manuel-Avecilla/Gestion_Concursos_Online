from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('concursos-online/listar', views.concursos_listar, name='lista_concursos')
]
