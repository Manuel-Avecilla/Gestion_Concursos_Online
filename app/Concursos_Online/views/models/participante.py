# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from Concursos_Online.models import Participante
from Concursos_Online.forms import ParticipanteForm, ParticipanteBuscarAvanzada
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

# endregion
# ============================================================




# ============================================================
# region Pages
# ============================================================


#region --- Detalles Participante ---
def dame_participante(request, id_participante):
    
    participante = (
        Participante.objects
        .get(id=id_participante)
    )
    
    return render(request,'models/participantes/participante_detalle.html',{'Participante_Mostrar':participante})
# endregion

#region --- Lista Participante ---
def participantes_listar(request):
    participantes = (
        Participante.objects
        .select_related("usuario")
        .all()
    )
    return render(request,'models/participantes/lista_participantes.html',{'Participantes_Mostrar':participantes})
# endregion

#region --- Filtros Participante ---
def dame_participantes_concurso(request, id_concurso):
    
    participantes = (
        Participante.objects
        .select_related("usuario")
        .filter(inscribe_participante__concurso_id=id_concurso)
        .all()
        .distinct()
    )
    
    return render(request,'models/participantes/lista_participantes.html',{'Participantes_Mostrar':participantes})

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
# endregion


# endregion
# ============================================================




# ============================================================
# region CRUD (Create, Read, Update, Delete)
# ============================================================

#region --- CREATE ---
@permission_required('Concursos_Online.add_participante', raise_exception=True)
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
#endregion

#region --- READ ---
@permission_required('Concursos_Online.view_participante', raise_exception=True)
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
#endregion

#region --- UPDATE ---
@permission_required('Concursos_Online.change_participante', raise_exception=True)
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
#endregion

#region --- DELETE ---
@permission_required('Concursos_Online.delete_participante', raise_exception=True)
def participante_eliminar(request, id_participante): # Eliminar Perfil
    participante = Participante.objects.get(id = id_participante)
    nombre = participante.alias
    try:
        participante.delete()
        messages.success(request, 'Se ha eliminado el Participante [ '+nombre+' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('participantes_listar')
#endregion

# endregion
# ============================================================