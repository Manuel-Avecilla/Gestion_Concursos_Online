# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render
from Concursos_Online.models import Concurso
from Concursos_Online.forms import ConcursoForm, ConcursoBuscarAvanzada
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

from django.contrib import messages
from django.shortcuts import redirect

# endregion
# ============================================================




# ============================================================
# region Pages
# ============================================================


#region --- Detalles Concurso ---
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
#endregion

#region --- Lista Concurso ---
def concursos_listar(request):
    
    concursos = (
        Concurso.objects
        .select_related(
            "creador__usuario",  # anidado
            "ganador__usuario",  # Asi también accedes a su usuario
        )
        .prefetch_related("participantes__usuario")
        .prefetch_related("creador__usuario")
        .prefetch_related("ganador__usuario")  # Relacion N:N en participantes
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
#endregion

#region --- Filtros Concurso ---

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

#endregion


# endregion
# ============================================================




# ============================================================
# region CRUD (Create, Read, Update, Delete)
# ============================================================

#region --- CREATE ---
@permission_required('Concursos_Online.add_concurso', raise_exception=True)
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
            return redirect('concursos_listar')

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
#endregion

#region --- READ ---
@permission_required('Concursos_Online.view_concurso', raise_exception=True)
def concurso_buscar_avanzado(request):  # Búsqueda Avanzada para Concurso

    if len(request.GET) > 0:
        formulario = ConcursoBuscarAvanzada(request.GET)
        if formulario.is_valid():

            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsConcurso = (
                Concurso.objects
                .prefetch_related("participantes__usuario")
                .prefetch_related("creador__usuario")
                .prefetch_related("ganador__usuario")
            )
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
#endregion

#region --- UPDATE ---
@permission_required('Concursos_Online.change_concurso', raise_exception=True)
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
            return redirect('concursos_listar')
    
    return render(request, 'models/concursos/crud/actualizar_concursos.html', {'formulario': formulario, 'concurso': concurso})
#endregion

#region --- DELETE ---
@permission_required('Concursos_Online.delete_concurso', raise_exception=True)
def concurso_eliminar(request, id_concurso):  # Eliminar Concurso
    concurso = Concurso.objects.get(id=id_concurso)
    nombre = concurso.nombre
    try:
        concurso.delete()
        messages.success(request, 'Se ha eliminado el Concurso [ ' + nombre + ' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('concursos_listar')
#endregion

# endregion
# ============================================================

