from django.shortcuts import render
from .models import *
from django.db.models import Q , Prefetch, Avg, Max, Min
from django.views.defaults import page_not_found

from .forms import *
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def home(request):
    return render(request, 'pages/home.html')

def menu(request):
    return render(request, 'pages/menu.html')

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
    
    return render(request,'concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

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
    
    return render(request,'concursos/concurso_detalle.html',{'Concurso_Mostrar':concurso})

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
    
    return render(request,'concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

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
    
    return render(request,'concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

# Una url que:
# Lista los concursos que tienen el texto especificado en su descripción.
# Los concursos resultantes están ordenados de forma descendente (de Z a A) según el nombre.
def dame_concurso_texto(request, texto):
    
    concursos = (
        Concurso.objects
        .select_related(
            "creador__usuario",  # anidado
            "ganador__usuario",  # Asi también accedes a su usuario
        )
        .prefetch_related("participantes__usuario")  # Relacion N:N en participantes
    )
    concursos = concursos.filter(descripcion__contains=texto).order_by("-nombre")
    concursos.all()
    
    """
    # 1. Prepara el parámetro para la búsqueda de subcadena (LIKE '%%')
    texto_con_comodines = '%' + texto + '%'
    
    concursos = (Concurso.objects.raw(
    "SELECT * FROM Concursos_Online_concurso co "
    + " JOIN Concursos_Online_administrador ad ON co.creador_id = ad.id "
    + " JOIN Concursos_Online_participante pa ON co.ganador_id = pa.id "
    + " JOIN Concursos_Online_inscribe ins ON co.id = ins.concurso_id "
    + " JOIN Concursos_Online_participante p ON p.id = ins.participante_id "
    + " WHERE co.descripcion LIKE %s "
    + " ORDER BY co.nombre DESC "
    ,[texto_con_comodines] # Usamos la variable texto_con_comodines
    ))
    """
    
    return render(request,'concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

# Una url que permite ver el participante que se inscribió más recientemente en un concurso concreto, utilizando el ID del concurso.
# Muestra únicamente la información de ese último inscrito, limitando la consulta a un solo registro
def dame_ultimo_participante(request, id_concurso):
    
    participante_a_mostrar = (
        Participante.objects
        .filter(inscribe_participante__concurso_id = id_concurso)
        .order_by("-inscribe_participante__fecha_inscripcion")[:1].get()
    )
    
    """
    participante_raw = (Participante.objects.raw(
    "SELECT * FROM Concursos_Online_participante pa "
    + " JOIN Concursos_Online_inscribe ins ON pa.id = ins.participante_id "
    + " WHERE ins.concurso_id = %s " 
    + " ORDER BY ins.fecha_inscripcion DESC "
    + " LIMIT 1 " 
    ,[id_concurso] 
    ))
    # --- Extraer el objeto único ---
    try:
        # Usamos next(iter(participante_raw)) para obtener el objeto singular.
        # next(iter()) maneja el caso de lista vacía limpiamente.
        participante_a_mostrar = next(iter(participante_raw))
    except StopIteration:
        # Esto ocurre si LIMIT 1 no encontró ningún resultado para ese id_concurso
        participante_a_mostrar = None
        
    # El diccionario ahora envía el objeto Participante individual (o None)
    """
    return render(request,'participantes/participante_detalle.html',{'Participante_Mostrar':participante_a_mostrar})

# Una url que permite obtener información sobre un Participante en concreto, buscando por su alias.
def detalle_participante_alias(request, alias_participante):
    
    participante_a_mostrar = (
        Participante.objects
        .get(alias=alias_participante)
    )
    
    """
    participante_a_mostrar = (Participante.objects.raw(
    "SELECT * FROM Concursos_Online_participante pa "
    + " WHERE pa.alias = %s "
    ,[alias_participante]
    )[0])
    """
    
    return render(request,'participantes/participante_detalle.html',{'Participante_Mostrar':participante_a_mostrar})

# Una url que obtiene todos los Usuarios que nunca han recibido una Notificación.
def usuarios_sin_notificar(request):
    
    usuarios_no_notificados = (
        Usuario.objects
        .filter(recibos=None)
    )
    usuarios_no_notificados.all()
    
    """
    usuarios_no_notificados = (Usuario.objects.raw(
    "SELECT * FROM Concursos_Online_usuario user "
    + " LEFT JOIN Concursos_Online_recibe re ON re.usuario_id = user.id "
    + " WHERE re.usuario_id IS NULL "
    ))
    """
    
    return render(request, 'usuarios/lista_usuarios.html',{'Usuarios_Mostrar':usuarios_no_notificados})

# Una url que obtiene todos los objetos Jurado.
def dame_jurados(request):
    
    jurados = (
        Jurado.objects
        .select_related('usuario') 
        .prefetch_related(Prefetch('concursos')) 
    )
    jurados.all()
    
    """
    jurados = (Jurado.objects.raw(
    "SELECT * FROM Concursos_Online_jurado ju "
    + " JOIN Concursos_Online_usuario user ON user.id = ju.usuario_id"
    + " LEFT JOIN Concursos_Online_asigna asig ON asig.jurado_id = ju.id "
    + " LEFT JOIN Concursos_Online_concurso co ON asig.concurso_id = co.id "
    ))
    """
    return render(request, 'jurados/lista_jurados.html', {'Jurados_Mostrar':jurados})

# Una url que calcula y muestra las métricas de agregación (media, máximo y mínimo) del campo experiencia de todos los Jurados.
def metricas_experiencia_jurados(request):
    
    metricas_objeto = (
        Jurado.objects
        .aggregate(
            media_experiencia=Avg('experiencia'),
            max_experiencia=Max('experiencia'),
            min_experiencia=Min('experiencia')
        )
    )
    
    """
    metricas_queryset = (Jurado.objects.raw(
    "SELECT 1 AS id, AVG(experiencia) AS media_experiencia, MAX(experiencia) AS max_experiencia, MIN(experiencia) AS min_experiencia FROM Concursos_Online_jurado"
    ))
    
    # Se debe obtener el único objeto del RawQuerySet iterable
    try:
        # Usamos next(iter(participante_raw)) para obtener el objeto singular.
        # next(iter()) maneja el caso de lista vacía limpiamente.
        metricas_objeto = next(iter(metricas_queryset))
    except IndexError:
        # En caso de que no haya jurados, maneja la excepción
        metricas_objeto = None
    """
    return render(request, 'jurados/metricas_jurados.html', {'Metricas_Mostrar':metricas_objeto})

def participantes_listar(request):
    participantes = (
        Participante.objects
        .select_related("usuario")
        .all()
    )
    return render(request,'participantes/lista_participantes.html',{'Participantes_Mostrar':participantes})

def dame_usuario(request, id_usuario):
    
    usuario = (
        Usuario.objects
        .get(id=id_usuario)
    )
    
    return render(request, 'usuarios/usuario_detalle.html',{'Usuario_Mostrar':usuario})

def dame_jurado(request, id_jurado):
    
    jurado = (
        Jurado.objects
        .select_related('usuario') 
        .prefetch_related(Prefetch('concursos')) 
        .get(id=id_jurado)
    )
    
    return render(request, 'jurados/jurado_detalle.html',{'Jurado_Mostrar':jurado})

def dame_participantes_concurso(request, id_concurso):
    
    participantes = (
        Participante.objects
        .select_related("usuario")
        .filter(inscribe_participante__concurso_id=id_concurso)
        .all()
        .distinct()
    )
    
    return render(request,'participantes/lista_participantes.html',{'Participantes_Mostrar':participantes})

#--------------------------------------------------------------------------------------------
#                                          CRUD
#--------------------------------------------------------------------------------------------

#-------- USUARIO --------
def usuario_create(request): # Metodo que controla el formulario
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = UsuarioForm(datosFormulario)
    
    if (request.method == "POST"):
        
        libro_creado = crear_usuario_modelo(formulario)
        
        if(libro_creado):
            messages.success(request, 'Se ha creado el Usuario '+formulario.cleaned_data.get('nombre_usuario')+" correctamente")
            return redirect('home')

    return render(request, 'usuarios/crud/create_usuario.html',{'formulario':formulario})

def crear_usuario_modelo(formulario): # Metodo que crea en la base de datos
    
    usuario_creado = False
    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Guarda el usuario en la base de datos
            formulario.save()
            usuario_creado = True
        except Exception as error:
            print(error)
    return usuario_creado

#--------------------------

# Errores

def mi_error_404(request,exception=None):
    return render(request,'error/404.html',None,None,404)

def mi_error_403(request,exception=None):
    return render(request,'error/403.html',None,None,403)

def mi_error_400(request,exception=None):
    return render(request,'error/400.html',None,None,400)

def mi_error_500(request,exception=None):
    return render(request,'error/500.html',None,None,500)