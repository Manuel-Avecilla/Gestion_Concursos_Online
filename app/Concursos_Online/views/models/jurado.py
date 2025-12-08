# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from Concursos_Online.models import Jurado
from Concursos_Online.forms import JuradoForm, JuradoBuscarAvanzada
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Prefetch, Avg, Max, Min

# endregion
# ============================================================




# ============================================================
# region Pages
# ============================================================


#region --- Detalles Jurado ---
def dame_jurado(request, id_jurado):
    
    jurado = (
        Jurado.objects
        .select_related('usuario') 
        .prefetch_related(Prefetch('concursos')) 
        .get(id=id_jurado)
    )
    
    return render(request, 'models/jurados/jurado_detalle.html',{'Jurado_Mostrar':jurado})
# endregion

#region --- Lista Jurado ---
def jurados_listar(request):
    
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
# endregion

#region --- Filtros Jurado ---

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

# endregion


# endregion
# ============================================================




# ============================================================
# region CRUD (Create, Read, Update, Delete)
# ============================================================

#region --- CREATE ---
@permission_required('concursos_online.add_jurado', raise_exception=True)
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
            nombre = usuario.username
            
            messages.success(request, 'Se ha creado el Jurado: [ ' + nombre + " ] correctamente.")
            return redirect('jurados_listar')

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
#endregion

#region --- READ ---
@permission_required('concursos_online.view_jurado', raise_exception=True)
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
                QsJurado = QsJurado.filter(usuario__username__icontains=usuario_contiene)
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
#endregion

#region --- UPDATE ---
@permission_required('concursos_online.change_jurado', raise_exception=True)
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
            nombre = usuario.username
            
            messages.success(request, 'Se ha actualizado el Jurado: [ ' + nombre + " ] correctamente.")
            return redirect('jurados_listar')
    
    return render(
        request,
        'models/jurados/crud/actualizar_jurados.html',
        {
            'formulario': formulario,
            'jurado': jurado
        }
    )
#endregion

#region --- DELETE ---
@permission_required('concursos_online.delete_jurado', raise_exception=True)
def jurado_eliminar(request, id_jurado):  # Eliminar Jurado
    jurado = Jurado.objects.get(id=id_jurado)
    nombre = jurado.usuario.username
    
    try:
        jurado.delete()
        messages.success(request, 'Se ha eliminado el Jurado [ ' + nombre + ' ] correctamente.')
    except Exception as error:
        print(error)
    
    return redirect('jurados_listar')
#endregion

# endregion
# ============================================================