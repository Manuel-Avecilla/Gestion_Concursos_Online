# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from Concursos_Online.models import Perfil
from Concursos_Online.forms import PerfilForm, PerfilBuscarAvanzada
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from datetime import datetime

# endregion
# ============================================================




# ============================================================
# region Pages
# ============================================================


#region --- Detalles Perfil ---
def dame_perfil(request, id_perfil):
    
    perfil = (
        Perfil.objects
        .get(id=id_perfil)
    )
    
    return render(request, 'models/perfil/perfil_detalle.html',{'Perfil_Mostrar':perfil})
# endregion

#region --- Lista Perfil ---
def perfiles_listar(request):
    
    perfil = (
        Perfil.objects
        .select_related("usuario")
        .all()
    )
    return render(request,'models/perfil/lista_perfil.html',{'Perfiles_Mostrar':perfil})
# endregion

#region --- Filtros Perfil ---
# endregion


# endregion
# ============================================================




# ============================================================
# region CRUD (Create, Read, Update, Delete)
# ============================================================

#region --- CREATE ---
@permission_required('concursos_online.add_perfil', raise_exception=True)
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

@permission_required('concursos_online.add_perfil', raise_exception=True)
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
#endregion

#region --- READ ---
@permission_required('concursos_online.view_perfil', raise_exception=True)
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
#endregion

#region --- UPDATE ---
@permission_required('concursos_online.change_perfil', raise_exception=True)
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
#endregion

#region --- DELETE ---
@permission_required('concursos_online.delete_perfil', raise_exception=True)
def perfil_eliminar(request, id_perfil): # Eliminar Perfil
    perfil = Perfil.objects.get(id = id_perfil)
    nombre = perfil.nombre_completo
    try:
        perfil.delete()
        messages.success(request, 'Se ha eliminado el Perfil [ '+nombre+' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('perfiles_listar')
#endregion

# endregion
# ============================================================