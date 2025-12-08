# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from Concursos_Online.models import Administrador
from Concursos_Online.forms import AdministradorForm, AdministradorBuscarAvanzada
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

# endregion
# ============================================================




# ============================================================
# region Pages
# ============================================================

#region --- Detalles Administrador ---
def dame_administrador(request, id_administrador):
    
    administrador = (
        Administrador.objects
        .get(id=id_administrador)
    )
    
    return render(request, 'models/administradores/administrador_detalle.html',{'Administrador_Mostrar':administrador})
# endregion

#region --- Lista Administrador ---
def administradores_listar(request):
    
    administradores = (
        Administrador.objects
        .select_related("usuario")
        .all()
    )
    return render(request,'models/administradores/lista_administradores.html',{'Administradores_Mostrar':administradores})
# endregion

# endregion
# ============================================================




# ============================================================
# region CRUD (Create, Read, Update, Delete)
# ============================================================


#region --- CREATE ---
@permission_required('concursos_online.add_administrador', raise_exception=True)
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
#endregion

#region --- READ ---
@permission_required('concursos_online.add_administrador', raise_exception=True)
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

@permission_required('concursos_online.view_administrador', raise_exception=True)
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
#endregion

#region --- UPDATE ---
@permission_required('concursos_online.change_administrador', raise_exception=True)
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
#endregion

#region --- DELETE ---
@permission_required('concursos_online.delete_administrador', raise_exception=True)
def administrador_eliminar(request, id_administrador):  # Eliminar Administrador
    administrador = Administrador.objects.get(id=id_administrador)
    nombre = administrador.usuario.nombre_usuario
    try:
        administrador.delete()
        messages.success(request, 'Se ha eliminado el Administrador [ ' + nombre + ' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('administradores_listar')
#endregion


# endregion
# ============================================================