from django.shortcuts import render
from .models import *
from django.db.models import Q
# Create your views here.

def index(request):
    return render(request, 'Concursos_Online/index.html')

# Una url que me muestre todos los Concursos y sus datos, incluido los relacionados.
def concursos_listar(request):
    
    concursos = (
        Concurso.objects
        .select_related(
            "creador__usuario",  # anidado
            "ganador__usuario",  # Asi también accedes a su usuario
        )
        .prefetch_related("participantes__usuario")  # Relacion N:N en participantes
    )
    concursos.all()
    
    """
    concursos = (Concurso.objects.raw(
    "SELECT * FROM Concursos_Online_concurso co "
    + " JOIN Concursos_Online_administrador ad ON co.creador_id = ad.id "
    + " JOIN Concursos_Online_participante pa ON co.ganador_id = pa.id "
    + " JOIN Concursos_Online_inscribe ins ON co.id = ins.concurso_id "
    + " JOIN Concursos_Online_participante p ON p.id = ins.participante_id"
    ))
    """
    
    return render(request,'Concursos_Online/lista_Concurso.html',{'Concursos_Mostrar':concursos})

# Una url que me muestre un Concurso y sus datos, incluido los relacionados.
def dame_concurso(request, id_concurso):
    
    concurso = (
        Concurso.objects
        .select_related(
            "creador__usuario",  # anidado
            "ganador__usuario",  # Asi también accedes a su usuario
        )
        .prefetch_related("participantes__usuario")  # Relacion N:N en participantes
        .get(id=id_concurso) # Obtiene el concurso con el ID especificado
    )
    
    """
    concurso = (Concurso.objects.raw(
    "SELECT * FROM Concursos_Online_concurso co "
    + " JOIN Concursos_Online_administrador ad ON co.creador_id = ad.id "
    + " JOIN Concursos_Online_participante pa ON co.ganador_id = pa.id "
    + " JOIN Concursos_Online_inscribe ins ON co.id = ins.concurso_id "
    + " JOIN Concursos_Online_participante p ON p.id = ins.participante_id"
    + " WHERE co.id = %s",[id_concurso])[0]
    )
    """
    
    return render(request,'Concursos_Online/Concurso.html',{'Concurso_Mostrar':concurso})

# Una url que muestre los Concursos que comienzan en un año y mes concreto
def dame_concursos_fecha(request, anyo_concurso, mes_concurso):
    
    concursos = (
        Concurso.objects
        .select_related(
            "creador__usuario",  # anidado
            "ganador__usuario",  # Asi también accedes a su usuario
        )
        .prefetch_related("participantes__usuario")  # Relacion N:N en participantes
    )
    concursos = concursos.filter(fecha_inicio__year=anyo_concurso, fecha_inicio__month=mes_concurso)
    concursos.all()
    
    """
    # Convertir el mes a cadena y asegurar que tenga 2 digitos con relleno de cero
    mes_formato_sql = str(mes_concurso).zfill(2)
    
    concursos = (Concurso.objects.raw(
    "SELECT * FROM Concursos_Online_concurso co "
    + " JOIN Concursos_Online_administrador ad ON co.creador_id = ad.id "
    + " JOIN Concursos_Online_participante pa ON co.ganador_id = pa.id "
    + " JOIN Concursos_Online_inscribe ins ON co.id = ins.concurso_id "
    + " JOIN Concursos_Online_participante p ON p.id = ins.participante_id"
    + " WHERE strftime('%%Y', co.fecha_inicio) = %s "
    + " AND strftime('%%m', co.fecha_inicio) = %s "
    ,[str(anyo_concurso),mes_formato_sql] # Usamos la variable formateada
    ))
    """
    
    return render(request,'Concursos_Online/lista_Concurso.html',{'Concursos_Mostrar':concursos})

# Una url que:
# Si pones "true" en la URL, solo ves los concursos activos;
# Si pones "false", ves todos los concursos (activos e inactivos);
# Y siempre están ordenados por fecha de inicio.
def dame_concurso_activo(request, activo):
    
    # Variable para transformar el str de la url a bolean
    is_active = (str(activo).lower() == 'true')
    
    concursos = (
        Concurso.objects
        .select_related(
            "creador__usuario",  # anidado
            "ganador__usuario",  # Asi también accedes a su usuario
        )
        .prefetch_related("participantes__usuario")  # Relacion N:N en participantes
    )
    concursos = concursos.filter(Q(activo=is_active)|Q(activo=True)).order_by("fecha_inicio")
    concursos.all()
    
    """
    concursos = (Concurso.objects.raw(
    "SELECT * FROM Concursos_Online_concurso co "
    + " JOIN Concursos_Online_administrador ad ON co.creador_id = ad.id "
    + " JOIN Concursos_Online_participante pa ON co.ganador_id = pa.id "
    + " JOIN Concursos_Online_inscribe ins ON co.id = ins.concurso_id "
    + " JOIN Concursos_Online_participante p ON p.id = ins.participante_id"
    + " WHERE co.activo = %s "
    + " OR co.activo = True "
    + " ORDER BY co.fecha_inicio "
    ,[is_active] # Usamos la variable activo
    ))
    """
    
    return render(request,'Concursos_Online/lista_Concurso.html',{'Concursos_Mostrar':concursos})