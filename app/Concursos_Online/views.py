from django.shortcuts import render
from .models import *
from django.db.models import Q , Prefetch, Avg, Max, Min
from django.views.defaults import page_not_found

from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from datetime import datetime

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
    
    return render(request,'models/concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

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
    
    return render(request,'models/concursos/concurso_detalle.html',{'Concurso_Mostrar':concurso})

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
    
    return render(request,'models/concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

# Una url que:
# Si pones "true" en la URL, solo ves los concursos activos;
# Si pones "false", ves todos los concursos (activos e inactivos);
# Y siempre están ordConcursoenados por fecha de inicio.
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
    
    return render(request,'models/concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

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
    
    return render(request,'models/concursos/lista_concursos.html',{'Concursos_Mostrar':concursos})

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
    return render(request,'models/participantes/participante_detalle.html',{'Participante_Mostrar':participante_a_mostrar})

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
    
    return render(request,'models/participantes/participante_detalle.html',{'Participante_Mostrar':participante_a_mostrar})

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
    
    return render(request, 'models/usuarios/lista_usuarios.html',{'Usuarios_Mostrar':usuarios_no_notificados})

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
    return render(request, 'models/jurados/lista_jurados.html', {'Jurados_Mostrar':jurados})

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
    return render(request, 'models/jurados/metricas_jurados.html', {'Metricas_Mostrar':metricas_objeto})

def participantes_listar(request):
    participantes = (
        Participante.objects
        .select_related("usuario")
        .all()
    )
    return render(request,'models/participantes/lista_participantes.html',{'Participantes_Mostrar':participantes})

def dame_usuario(request, id_usuario):
    
    usuario = (
        Usuario.objects
        .get(id=id_usuario)
    )
    
    return render(request, 'models/usuarios/usuario_detalle.html',{'Usuario_Mostrar':usuario})

def dame_jurado(request, id_jurado):
    
    jurado = (
        Jurado.objects
        .select_related('usuario') 
        .prefetch_related(Prefetch('concursos')) 
        .get(id=id_jurado)
    )
    
    return render(request, 'models/jurados/jurado_detalle.html',{'Jurado_Mostrar':jurado})

def dame_participantes_concurso(request, id_concurso):
    
    participantes = (
        Participante.objects
        .select_related("usuario")
        .filter(inscribe_participante__concurso_id=id_concurso)
        .all()
        .distinct()
    )
    
    return render(request,'models/participantes/lista_participantes.html',{'Participantes_Mostrar':participantes})

def dame_perfil(request, id_perfil):
    
    perfil = (
        Perfil.objects
        .get(id=id_perfil)
    )
    
    return render(request, 'models/perfil/perfil_detalle.html',{'Perfil_Mostrar':perfil})

def perfiles_listar(request):
    
    perfil = (
        Perfil.objects
        .select_related("usuario")
        .all()
    )
    return render(request,'models/perfil/lista_perfil.html',{'Perfiles_Mostrar':perfil})

def dame_administrador(request, id_administrador):
    
    administrador = (
        Administrador.objects
        .get(id=id_administrador)
    )
    
    return render(request, 'models/administradores/administrador_detalle.html',{'Administrador_Mostrar':administrador})

def administradores_listar(request):
    
    administradores = (
        Administrador.objects
        .select_related("usuario")
        .all()
    )
    return render(request,'models/administradores/lista_administradores.html',{'Administradores_Mostrar':administradores})


#--------------------------------------------------------------------------------------------
#                                          CRUD
#--------------------------------------------------------------------------------------------

#-------- USUARIO --------
def usuario_create(request): # Metodo que controla el tipo de formulario
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = UsuarioForm(datosFormulario)
    
    if (request.method == "POST"):
        
        usuario_creado = crear_usuario_modelo(formulario)
        
        if(usuario_creado):
            messages.success(request, 'Se ha creado el Usuario: [ '+formulario.cleaned_data.get('nombre_usuario')+" ] correctamente.")
            return redirect('usuario_buscar')

    return render(request, 'models/usuarios/crud/create_usuario.html',{'formulario':formulario})

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

def usuario_buscar(request): # Busqueda Simple

    texto = request.GET.get("textoBusqueda", "")  # vacio si no se envia nada
    
    # Equivalente al TRIM (Elimina espacios del principio y final)
    texto = texto.strip()

    if texto:
        usuarios = Usuario.objects.filter(
            Q(nombre_usuario__icontains=texto) |
            Q(correo__icontains=texto)
        )
    else:
        usuarios = Usuario.objects.all()

    return render(request,'models/usuarios/lista_usuarios.html',{'Usuarios_Mostrar': usuarios,'Texto_Busqueda': texto,})

def usuario_buscar_avanzado(request): #Busqueda Avanzada
    
    if(len(request.GET) > 0):
        formulario = UsuarioBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsUsuarios = Usuario.objects
            
            #Obtenemos los filtros
            nombre_usuario_contiene = formulario.cleaned_data.get('nombre_usuario_contiene')
            correo_contiene = formulario.cleaned_data.get('correo_contiene')
            fecha_registro_desde = formulario.cleaned_data.get('fecha_registro_desde')
            fecha_registro_hasta = formulario.cleaned_data.get('fecha_registro_hasta')
            tipo_usuario = formulario.cleaned_data.get('tipo_usuario')
            
            #---Nombre---
            if(nombre_usuario_contiene!=''):
                nombre_usuario_contiene = nombre_usuario_contiene.strip()
                QsUsuarios = QsUsuarios.filter(nombre_usuario__icontains=nombre_usuario_contiene)
                mensaje_busqueda += '· Nombre contiene "'+nombre_usuario_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier nombre \n'
            
            #---Correo---
            if(correo_contiene!=''):
                correo_contiene = correo_contiene.strip()
                QsUsuarios = QsUsuarios.filter(correo__icontains=correo_contiene)
                mensaje_busqueda += '· Correo contiene "'+correo_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier correo \n'
            
            #---Fecha---
            if (not fecha_registro_desde is None):
                QsUsuarios = QsUsuarios.filter(fecha_registro__gte=fecha_registro_desde)
                mensaje_busqueda += '· Registro desde '+datetime.strftime(fecha_registro_desde,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· Registro desde: Cualquier fecha \n'
            
            if (not fecha_registro_hasta is None):
                QsUsuarios = QsUsuarios.filter(fecha_registro__lte=fecha_registro_hasta)
                mensaje_busqueda += '· Registro hasta '+datetime.strftime(fecha_registro_hasta,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· Registro hasta: Cualquier fecha \n'
            
            #---Tipo---
            if tipo_usuario == 'admin':
                QsUsuarios = QsUsuarios.filter(administrador__isnull=False)
                mensaje_busqueda += '· Rol: Admin \n'

            elif tipo_usuario == 'jurado':
                QsUsuarios = QsUsuarios.filter(jurado__isnull=False)
                mensaje_busqueda += '· Rol: Jurado \n'

            elif tipo_usuario == 'participante':
                QsUsuarios = QsUsuarios.filter(participante__isnull=False)
                mensaje_busqueda += '· Rol: Participante \n'
            
            else:
                mensaje_busqueda += '· Rol: Cualquiera \n'
            
            #Ejecutamos la querySet y enviamos los usuarios
            usuarios = QsUsuarios.all()
            
            return render(request, 'models/usuarios/lista_usuarios.html',
                        {'Usuarios_Mostrar':usuarios,
                        'Mensaje_Busqueda':mensaje_busqueda}
                        )
    else:
        formulario = UsuarioBuscarAvanzada(None)
    return render(request, 'models/usuarios/crud/buscar_avanzada_usuarios.html',{'formulario':formulario})

def usuario_editar(request, id_usuario): # Editar Usuario
    usuario = Usuario.objects.get(id = id_usuario)
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = UsuarioForm(datosFormulario,instance=usuario)
    
    if (request.method == "POST"):
        
        usuario_creado = crear_usuario_modelo(formulario)
        
        if(usuario_creado):
            messages.success(request, 'Se ha actualizado el Usuario: [ '+formulario.cleaned_data.get('nombre_usuario')+" ] correctamente.")
            return redirect('usuario_buscar')
    
    return render(request, 'models/usuarios/crud/actualizar_usuario.html', {'formulario':formulario,'usuario':usuario})

def usuario_eliminar(request, id_usuario): # Eliminar Usuario
    usuario = Usuario.objects.get(id=id_usuario)
    nombre = usuario.nombre_usuario
    try:
        usuario.delete()
        messages.success(request, 'Se ha eliminado el Usuario [ '+nombre+' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('usuario_buscar')
#--------------------------

#-------- PERFIL ----------
def perfil_create(request): #Metodo que controla el tipo de formulario
        
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    mediaFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        mediaFormulario = request.FILES
    
    formulario = PerfilForm(datosFormulario, mediaFormulario)
    
    if (request.method == "POST"):
        
        perfil_creado = crear_perfil_modelo(formulario)
        
        if(perfil_creado):
            messages.success(request, 'Se ha creado el Perfil: [ '+formulario.cleaned_data.get('nombre_completo')+" ] correctamente.")
            return redirect('perfiles_listar')

    return render(request, 'models/perfil/crud/create_perfil.html',{'formulario':formulario})

def crear_perfil_modelo(formulario): #Metodo que interactua con la base de datos
    
    perfil_creado = False
    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Guarda el usuario en la base de datos
            formulario.save()
            perfil_creado = True
        except Exception as error:
            print(error)
    return perfil_creado

def perfil_buscar_avanzado(request): #Busqueda Avanzada
    
    if(len(request.GET) > 0):
        formulario = PerfilBuscarAvanzada(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsPerfil = Perfil.objects
            
            #Obtenemos los filtros
            biografia_contiene = formulario.cleaned_data.get('biografia_contiene')
            fecha_nacimiento_desde = formulario.cleaned_data.get('fecha_nacimiento_desde')
            fecha_nacimiento_hasta = formulario.cleaned_data.get('fecha_nacimiento_hasta')
            usuarios = formulario.cleaned_data.get('usuarios')
            
            #---Biografia---
            if(biografia_contiene!=''):
                biografia_contiene = biografia_contiene.strip()
                QsPerfil = QsPerfil.filter(biografia__icontains=biografia_contiene)
                mensaje_busqueda += '· Biografia contiene "'+biografia_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier Biografia \n'
            
            #---Fecha-Nacimiento---
            if (not fecha_nacimiento_desde is None):
                QsPerfil = QsPerfil.filter(fecha_nacimiento__gte=fecha_nacimiento_desde)
                mensaje_busqueda += '· Fecha Nacimiento desde '+datetime.strftime(fecha_nacimiento_desde,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· Fecha Nacimiento desde: Cualquier fecha \n'
            
            if (not fecha_nacimiento_hasta is None):
                QsPerfil = QsPerfil.filter(fecha_nacimiento__lte=fecha_nacimiento_hasta)
                mensaje_busqueda += '· Fecha Nacimiento hasta '+datetime.strftime(fecha_nacimiento_hasta,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· Fecha Nacimiento hasta: Cualquier fecha \n'
            
            #---Usuarios---
            if usuarios:
                QsPerfil = QsPerfil.filter(usuario__id__in=usuarios)
                
                # Recorre los nombres y los separa con ,
                nombres_usuarios = ", ".join([u.nombre_usuario for u in usuarios])
                mensaje_busqueda += f'· Perfil de los usuarios: {nombres_usuarios}\n'
                
            else:
                mensaje_busqueda += '· Perfil de cualquier usuario \n'
            
            
            #Ejecutamos la querySet y enviamos los usuarios
            perfiles = QsPerfil.all()
            
            return render(request, 'models/perfil/lista_perfil.html',
                        {'Perfiles_Mostrar':perfiles,
                        'Mensaje_Busqueda':mensaje_busqueda}
                        )
    else:
        formulario = PerfilBuscarAvanzada(None)
    return render(request, 'models/perfil/crud/buscar_avanzada_perfil.html',{'formulario':formulario})

def perfil_editar(request, id_perfil): # Editar Perfil
    
    perfil = Perfil.objects.get(id = id_perfil)
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    mediaFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        mediaFormulario = request.FILES
    
    formulario = PerfilForm(datosFormulario,mediaFormulario,instance=perfil)
    
    if (request.method == "POST"):
        
        perfil_creado = crear_perfil_modelo(formulario)
        
        if(perfil_creado):
            messages.success(request, 'Se ha actualizado el Perfil: [ '+formulario.cleaned_data.get('nombre_completo')+" ] correctamente.")
            return redirect('perfiles_listar')
    
    return render(request, 'models/perfil/crud/actualizar_perfil.html', {'formulario':formulario,'perfil':perfil})

def perfil_eliminar(request, id_perfil): # Eliminar Perfil
    perfil = Perfil.objects.get(id = id_perfil)
    nombre = perfil.nombre_completo
    try:
        perfil.delete()
        messages.success(request, 'Se ha eliminado el Perfil [ '+nombre+' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('perfiles_listar')
#--------------------------

#------ PARTICIPANTE ------
def participante_create(request): #Metodo que controla el tipo de formulario
        
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ParticipanteForm(datosFormulario)
    
    if (request.method == "POST"):
        
        participante_creado = crear_participante_modelo(formulario)
        
        if(participante_creado):
            messages.success(request, 'Se ha creado el Participante: [ '+formulario.cleaned_data.get('alias')+" ] correctamente.")
            return redirect('participantes_listar')

    return render(request, 'models/participantes/crud/create_participante.html',{'formulario':formulario})

def crear_participante_modelo(formulario): #Metodo que interactua con la base de datos
    
    participante_creado = False
    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Guarda el usuario en la base de datos
            formulario.save()
            participante_creado = True
        except Exception as error:
            print(error)
    return participante_creado

def participante_buscar_avanzado(request): #Busqueda Avanzada
    
    if(len(request.GET) > 0):
        formulario = ParticipanteBuscarAvanzada(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsParticipante = Participante.objects
            
            #Obtenemos los campos
            alias_contiene = formulario.cleaned_data.get('alias_contiene')
            edad_minima = formulario.cleaned_data.get('edad_minima')
            nivel_minimo = formulario.cleaned_data.get('nivel_minimo')
            
            #---Alias---
            if(alias_contiene!=''):
                alias_contiene = alias_contiene.strip()
                QsParticipante = QsParticipante.filter(alias__icontains=alias_contiene)
                mensaje_busqueda += '· Alias contiene "'+alias_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier Alias \n'
            
            #---Edad---
            if edad_minima is not None:
                QsParticipante = QsParticipante.filter(edad__gte=edad_minima)
                mensaje_busqueda += f'· Edad mínima: {edad_minima}\n'
            else:
                mensaje_busqueda += '· Cualquier edad\n'

            #---Nivel---
            if nivel_minimo is not None:
                QsParticipante = QsParticipante.filter(nivel__gte=nivel_minimo)
                mensaje_busqueda += f'· Nivel mínimo: {nivel_minimo}\n'
            else:
                mensaje_busqueda += '· Cualquier nivel\n'
            
            #Ejecutamos la querySet y enviamos los usuarios
            perfiles = QsParticipante.all()
            
            return render(request, 'models/participantes/lista_participantes.html',
                        {'Participantes_Mostrar':perfiles,
                        'Mensaje_Busqueda':mensaje_busqueda}
                        )
    else:
        formulario = ParticipanteBuscarAvanzada(None)
    return render(request, 'models/participantes/crud/buscar_avanzada_participantes.html',{'formulario':formulario})

def participante_editar(request, id_participante): # Actualizar Perfil
    
    participante = Participante.objects.get(id = id_participante)
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ParticipanteForm(datosFormulario,instance=participante)
    
    if (request.method == "POST"):
        
        participante_creado = crear_participante_modelo(formulario)
        
        if(participante_creado):
            messages.success(request, 'Se ha actualizado el Participante: [ '+formulario.cleaned_data.get('alias')+" ] correctamente.")
            return redirect('participantes_listar')
    
    return render(request, 'models/participantes/crud/actualizar_participantes.html', {'formulario':formulario,'participante':participante})

def participante_eliminar(request, id_participante): # Eliminar Perfil
    participante = Participante.objects.get(id = id_participante)
    nombre = participante.alias
    try:
        participante.delete()
        messages.success(request, 'Se ha eliminado el Participante [ '+nombre+' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('participantes_listar')
#--------------------------

#----- ADMINISTRADOR ------
def administrador_create(request):  # Metodo que controla el tipo de formulario
        
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = AdministradorForm(datosFormulario)
    
    if (request.method == "POST"):
        
        administrador_creado = crear_administrador_modelo(formulario)
        
        if (administrador_creado):
            
            usuario = formulario.cleaned_data.get('usuario')
            nombre = usuario.nombre_usuario
            
            messages.success(request, 'Se ha creado el Administrador: [ ' + nombre + " ] correctamente.")
            return redirect('administradores_listar')

    return render(request, 'models/administradores/crud/create_administrador.html', {'formulario': formulario})

def crear_administrador_modelo(formulario):  # Metodo que interactua con la base de datos
    
    administrador_creado = False
    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Guarda el administrador en la base de datos
            formulario.save()
            administrador_creado = True
        except Exception as error:
            print(error)
    return administrador_creado

def administrador_buscar_avanzado(request):  # Busqueda Avanzada

    if len(request.GET) > 0:
        formulario = AdministradorBuscarAvanzada(request.GET)

        if formulario.is_valid():

            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsAdministrador = Administrador.objects

            # Obtenemos los campos del formulario
            area_contiene = formulario.cleaned_data.get('area_contiene')
            activo = formulario.cleaned_data.get('activo')
            horario_minimo = formulario.cleaned_data.get('horario_minimo')
            horario_maximo = formulario.cleaned_data.get('horario_maximo')

            # --- Área Responsable ---
            if area_contiene != '':
                area_contiene = area_contiene.strip()
                QsAdministrador = QsAdministrador.filter(area_responsable__icontains=area_contiene)
                mensaje_busqueda += f'· Área responsable contiene "{area_contiene}"\n'
            else:
                mensaje_busqueda += '· Cualquier área responsable\n'

            # --- Estado Activo/Inactivo ---
            if activo == "1":
                QsAdministrador = QsAdministrador.filter(activo=True)
                mensaje_busqueda += '· Solo activos\n'
            elif activo == "0":
                QsAdministrador = QsAdministrador.filter(activo=False)
                mensaje_busqueda += '· Solo inactivos\n'
            else:
                mensaje_busqueda += '· Activos o inactivos (cualquiera)\n'

            # --- Horario después de ---
            if horario_minimo is not None:
                QsAdministrador = QsAdministrador.filter(horario_disponible__gte=horario_minimo)
                mensaje_busqueda += f'· Horario después de: {horario_minimo}\n'
            else:
                mensaje_busqueda += '· Cualquier horario inicial\n'

            # --- Horario antes de ---
            if horario_maximo is not None:
                QsAdministrador = QsAdministrador.filter(horario_disponible__lte=horario_maximo)
                mensaje_busqueda += f'· Horario antes de: {horario_maximo}\n'
            else:
                mensaje_busqueda += '· Cualquier horario final\n'

            # Ejecutamos el QuerySet final
            administradores = QsAdministrador.all()

            return render(
                request,
                'models/administradores/lista_administradores.html',
                {
                    'Administradores_Mostrar': administradores,
                    'Mensaje_Busqueda': mensaje_busqueda,
                }
            )
    else:
        formulario = AdministradorBuscarAvanzada(None)
    return render(
        request,
        'models/administradores/crud/buscar_avanzada_administradores.html',
        {'formulario': formulario}
    )

def administrador_editar(request, id_administrador):  # Actualizar Administrador
    
    administrador = Administrador.objects.get(id=id_administrador)
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = AdministradorForm(datosFormulario, instance=administrador)
    
    if (request.method == "POST"):
        
        administrador_actualizado = crear_administrador_modelo(formulario)
        
        if (administrador_actualizado):
            
            usuario = formulario.cleaned_data.get('usuario')
            nombre = usuario.nombre_usuario
            
            messages.success(request, 'Se ha actualizado el Administrador: [ ' + nombre + " ] correctamente.")
            return redirect('administradores_listar')
    
    return render(request, 'models/administradores/crud/actualizar_administradores.html', {'formulario': formulario, 'administrador': administrador})

def administrador_eliminar(request, id_administrador):  # Eliminar Administrador
    administrador = Administrador.objects.get(id=id_administrador)
    nombre = administrador.usuario.nombre_usuario
    try:
        administrador.delete()
        messages.success(request, 'Se ha eliminado el Administrador [ ' + nombre + ' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('administradores_listar')
#--------------------------

#-------- JURADO ----------
def jurado_create(request):  # Método que controla el tipo de formulario
        
    # Si la petición es GET se creará el formulario vacío
    # Si la petición es POST se creará el formulario con datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = JuradoForm(datosFormulario)
    
    if (request.method == "POST"):
        
        jurado_creado = crear_jurado_modelo(formulario)
        
        if (jurado_creado):
            
            usuario = formulario.cleaned_data.get('usuario')
            nombre = usuario.nombre_usuario
            
            messages.success(request, 'Se ha creado el Jurado: [ ' + nombre + " ] correctamente.")
            return redirect('dame_jurados')

    return render(request, 'models/jurados/crud/create_jurado.html', {'formulario': formulario})

def crear_jurado_modelo(formulario):  # Método que interactúa con la base de datos
    
    jurado_creado = False

    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Guarda el Jurado en la base de datos
            formulario.save()
            jurado_creado = True
        except Exception as error:
            print(error)
    
    return jurado_creado

def jurado_buscar_avanzado(request):  # Búsqueda Avanzada

    if len(request.GET) > 0:
        formulario = JuradoBuscarAvanzada(request.GET)

        if formulario.is_valid():

            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsJurado = Jurado.objects

            # Obtenemos los campos del formulario
            usuario_contiene = formulario.cleaned_data.get('usuario_contiene')
            especialidad_contiene = formulario.cleaned_data.get('especialidad_contiene')
            experiencia_minima = formulario.cleaned_data.get('experiencia_minima')
            puntuacion_minima = formulario.cleaned_data.get('puntuacion_minima')

            # --- Nombre de usuario contiene ---
            if usuario_contiene != '':
                usuario_contiene = usuario_contiene.strip()
                QsJurado = QsJurado.filter(usuario__nombre_usuario__icontains=usuario_contiene)
                mensaje_busqueda += f'· Usuario contiene "{usuario_contiene}"\n'
            else:
                mensaje_busqueda += '· Cualquier nombre de usuario\n'

            # --- Especialidad contiene ---
            if especialidad_contiene != '':
                especialidad_contiene = especialidad_contiene.strip()
                QsJurado = QsJurado.filter(especialidad__icontains=especialidad_contiene)
                mensaje_busqueda += f'· Especialidad contiene "{especialidad_contiene}"\n'
            else:
                mensaje_busqueda += '· Cualquier especialidad\n'

            # --- Experiencia mínima ---
            if experiencia_minima is not None:
                QsJurado = QsJurado.filter(experiencia__gte=experiencia_minima)
                mensaje_busqueda += f'· Experiencia mínima: {experiencia_minima} años\n'
            else:
                mensaje_busqueda += '· Cualquier experiencia\n'

            # --- Puntuación mínima ---
            if puntuacion_minima is not None:
                QsJurado = QsJurado.filter(puntuacion_media__gte=puntuacion_minima)
                mensaje_busqueda += f'· Puntuación mínima: {puntuacion_minima}\n'
            else:
                mensaje_busqueda += '· Cualquier puntuación\n'

            # Ejecutamos el QuerySet final
            jurados = QsJurado.all()

            return render(
                request,
                'models/jurados/lista_jurados.html',
                {
                    'Jurados_Mostrar': jurados,
                    'Mensaje_Busqueda': mensaje_busqueda,
                }
            )

    else:
        formulario = JuradoBuscarAvanzada(None)

    return render(
        request,
        'models/jurados/crud/buscar_avanzada_jurados.html',
        {'formulario': formulario}
    )

def jurado_editar(request, id_jurado):  # Actualizar Jurado
    
    jurado = Jurado.objects.get(id=id_jurado)
    
    # Si la petición es GET se creará el formulario vacío
    # Si la petición es POST se creará el formulario con datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = JuradoForm(datosFormulario, instance=jurado)
    
    if (request.method == "POST"):
        
        jurado_actualizado = crear_jurado_modelo(formulario)
        
        if (jurado_actualizado):
            
            usuario = formulario.cleaned_data.get('usuario')
            nombre = usuario.nombre_usuario
            
            messages.success(request, 'Se ha actualizado el Jurado: [ ' + nombre + " ] correctamente.")
            return redirect('dame_jurados')
    
    return render(
        request,
        'models/jurados/crud/actualizar_jurados.html',
        {
            'formulario': formulario,
            'jurado': jurado
        }
    )

def jurado_eliminar(request, id_jurado):  # Eliminar Jurado
    jurado = Jurado.objects.get(id=id_jurado)
    nombre = jurado.usuario.nombre_usuario
    
    try:
        jurado.delete()
        messages.success(request, 'Se ha eliminado el Jurado [ ' + nombre + ' ] correctamente.')
    except Exception as error:
        print(error)
    
    return redirect('dame_jurados')

#--------------------------

#-------- CONCURSO --------
def concurso_create(request):  # Método que controla el tipo de formulario

    # Si la petición es GET se creará el formulario vacío
    # Si la petición es POST se creará el formulario con datos.
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    formulario = ConcursoForm(datosFormulario)

    if (request.method == "POST"):

        concurso_creado = crear_concurso_modelo(formulario)

        if (concurso_creado):

            nombre_concurso = formulario.cleaned_data.get('nombre')

            messages.success(
                request,
                'Se ha creado el Concurso: [ ' + nombre_concurso + ' ] correctamente.'
            )
            return redirect('lista_concursos')

    return render(
        request,
        'models/concursos/crud/create_concurso.html',
        {'formulario': formulario}
    )

def crear_concurso_modelo(formulario):  # Método que interactúa con la base de datos
    
    concurso_creado = False

    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Guarda el Concurso en la base de datos
            formulario.save()
            concurso_creado = True
        except Exception as error:
            print(error)

    return concurso_creado

def concurso_buscar_avanzado(request):  # Búsqueda Avanzada para Concurso

    if len(request.GET) > 0:
        formulario = ConcursoBuscarAvanzada(request.GET)
        if formulario.is_valid():

            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsConcurso = Concurso.objects

            # Obtener valores del formulario
            nombre_contiene = formulario.cleaned_data.get('nombre_contiene')
            fecha_inicio_minima = formulario.cleaned_data.get('fecha_inicio_minima')
            fecha_final_maxima = formulario.cleaned_data.get('fecha_final_maxima')
            activo = formulario.cleaned_data.get('activo')

            # --- Nombre contiene ---
            if nombre_contiene != '':
                nombre_contiene = nombre_contiene.strip()
                QsConcurso = QsConcurso.filter(nombre__icontains=nombre_contiene)
                mensaje_busqueda += f'· Nombre contiene "{nombre_contiene}"\n'
            else:
                mensaje_busqueda += '· Cualquier nombre\n'

            # --- Fecha inicio desde ---
            if fecha_inicio_minima is not None:
                QsConcurso = QsConcurso.filter(fecha_inicio__gte=fecha_inicio_minima)
                mensaje_busqueda += f'· Desde fecha de inicio: {fecha_inicio_minima}\n'
            else:
                mensaje_busqueda += '· Cualquier fecha de inicio\n'

            # --- Fecha fin hasta ---
            if fecha_final_maxima is not None:
                QsConcurso = QsConcurso.filter(fecha_final__lte=fecha_final_maxima)
                mensaje_busqueda += f'· Hasta fecha fin: {fecha_final_maxima}\n'
            else:
                mensaje_busqueda += '· Cualquier fecha de fin\n'

            # --- Estado ---
            if activo == "1":
                QsConcurso = QsConcurso.filter(activo=True)
                mensaje_busqueda += '· Solo activos\n'
            elif activo == "0":
                QsConcurso = QsConcurso.filter(activo=False)
                mensaje_busqueda += '· Solo inactivos\n'
            else:
                mensaje_busqueda += '· Activos o inactivos (cualquiera)\n'

            # Query final
            concursos = QsConcurso.all()

            return render(
                request,
                'models/concursos/lista_concursos.html',
                {
                    'Concursos_Mostrar': concursos,
                    'Mensaje_Busqueda': mensaje_busqueda,
                }
            )
            
    else:
        formulario = ConcursoBuscarAvanzada(None)
    return render(
        request,
        'models/concursos/crud/buscar_avanzada_concursos.html',
        {'formulario': formulario}
    )

def concurso_editar(request, id_concurso):  # Actualizar Concurso
    
    concurso = Concurso.objects.get(id=id_concurso)
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = ConcursoForm(datosFormulario, instance=concurso)
    
    if (request.method == "POST"):
        
        concurso_actualizado = crear_concurso_modelo(formulario)
        
        if (concurso_actualizado):
            
            nombre = formulario.cleaned_data.get('nombre')
            
            messages.success(request, 'Se ha actualizado el Concurso: [ ' + nombre + " ] correctamente.")
            return redirect('lista_concursos')
    
    return render(request, 'models/concursos/crud/actualizar_concursos.html', {'formulario': formulario, 'concurso': concurso})

def concurso_eliminar(request, id_concurso):  # Eliminar Concurso
    concurso = Concurso.objects.get(id=id_concurso)
    nombre = concurso.nombre
    try:
        concurso.delete()
        messages.success(request, 'Se ha eliminado el Concurso [ ' + nombre + ' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('lista_concursos')
#--------------------------

#--------------------------------------------------------------------------------------------


# Errores

def mi_error_404(request,exception=None):
    return render(request,'error/404.html',None,None,404)

def mi_error_403(request,exception=None):
    return render(request,'error/403.html',None,None,403)

def mi_error_400(request,exception=None):
    return render(request,'error/400.html',None,None,400)

def mi_error_500(request,exception=None):
    return render(request,'error/500.html',None,None,500)