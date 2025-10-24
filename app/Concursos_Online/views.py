from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    return render(request, 'Concursos_Online/index.html')

def concursos_listar(request):
    concursos = Concurso.objects.select_related("creador").select_related("ganador").prefetch_related("participantes")
    concursos.all()
    """
    concursos = (Concurso.objects.raw(
    "SELECT * FROM Concursos_Online_concurso co "
    + " JOIN Concursos_Online_administrador ad ON co.creador = ad.id "
    + " JOIN Concursos_Online_participante pa ON co.ganador = pa.id "
    + " JOIN Concursos_Online_inscribe ins ON co.id = ins.concurso_id "
    + " JOIN Concursos_Online_participante p ON p.id = ins.participante_id"
    ))
    """
    return render(request,'Concursos_Online/lista_Concurso.html',{'Concursos_Mostrar':concursos})
