# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from Concursos_Online.models import Usuario
from Concursos_Online.forms import UsuarioForm, UsuarioBuscarAvanzada, RegistroForm
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

# endregion
# ============================================================




# ============================================================
# region Pages
# ============================================================


#region --- Detalles Usuario ---
def dame_usuario(request, id_usuario):
    
    usuario = (
        Usuario.objects
        .get(id=id_usuario)
    )
    
    return render(request, 'models/usuarios/usuario_detalle.html',{'Usuario_Mostrar':usuario})
# endregion

#region --- Lista Usuario ---
def usuarios_listar(request):
    
    usuarios = (
        Usuario.objects
        .all()
    )
    
    return render(request, 'models/usuarios/lista_usuarios.html',{'Usuarios_Mostrar':usuarios})
# endregion

#region --- Filtros Usuario ---

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

# endregion


# endregion
# ============================================================




# ============================================================
# region CRUD (Create, Read, Update, Delete)
# ============================================================

#region --- CREATE ---
@permission_required('concursos_online.add_usuario', raise_exception=True)
def usuario_create(request): # Metodo que controla el tipo de formulario
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = RegistroForm(datosFormulario)
    
    if (request.method == "POST"):
        
        usuario_creado = crear_usuario_modelo(formulario)
        
        if(usuario_creado):
            messages.success(request, 'Se ha creado el Usuario: [ '+formulario.cleaned_data.get('username')+" ] correctamente.")
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
# endregion

#region --- READ ---
@permission_required('concursos_online.view_usuario', raise_exception=True)
def usuario_buscar(request): # Busqueda Simple

    texto = request.GET.get("textoBusqueda", "")  # vacio si no se envia nada
    
    # Equivalente al TRIM (Elimina espacios del principio y final)
    texto = texto.strip()

    if texto:
        usuarios = Usuario.objects.filter(
            Q(username__icontains=texto) |
            Q(email__icontains=texto)
        )
    else:
        usuarios = Usuario.objects.all()

    return render(request,'models/usuarios/lista_usuarios.html',{'Usuarios_Mostrar': usuarios,'Texto_Busqueda': texto,})

@permission_required('concursos_online.view_usuario', raise_exception=True)
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
                QsUsuarios = QsUsuarios.filter(username__icontains=nombre_usuario_contiene)
                mensaje_busqueda += '· Nombre contiene "'+nombre_usuario_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier nombre \n'
            
            #---Correo---
            if(correo_contiene!=''):
                correo_contiene = correo_contiene.strip()
                QsUsuarios = QsUsuarios.filter(email__icontains=correo_contiene)
                mensaje_busqueda += '· Correo contiene "'+correo_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier correo \n'
            
            #---Fecha---
            if (not fecha_registro_desde is None):
                QsUsuarios = QsUsuarios.filter(date_joined__gte=fecha_registro_desde)
                mensaje_busqueda += '· Registro desde '+datetime.strftime(fecha_registro_desde,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· Registro desde: Cualquier fecha \n'
            
            if (not fecha_registro_hasta is None):
                QsUsuarios = QsUsuarios.filter(date_joined__lte=fecha_registro_hasta)
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
# endregion

#region --- UPDATE ---
@permission_required('concursos_online.change_usuario', raise_exception=True)
def usuario_editar(request, id_usuario): # Editar Usuario
    usuario = Usuario.objects.get(id = id_usuario)
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = RegistroForm(datosFormulario,instance=usuario)
    
    if (request.method == "POST"):
        
        usuario_creado = crear_usuario_modelo(formulario)
        
        if(usuario_creado):
            messages.success(request, 'Se ha actualizado el Usuario: [ '+formulario.cleaned_data.get('username')+" ] correctamente.")
            return redirect('usuario_buscar')
    
    return render(request, 'models/usuarios/crud/actualizar_usuario.html', {'formulario':formulario,'usuario':usuario})
# endregion

#region --- DELETE ---
@permission_required('concursos_online.delete_usuario', raise_exception=True)
def usuario_eliminar(request, id_usuario): # Eliminar Usuario
    usuario = Usuario.objects.get(id=id_usuario)
    nombre = usuario.username
    try:
        usuario.delete()
        messages.success(request, 'Se ha eliminado el Usuario [ '+nombre+' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('usuario_buscar')
#endregion

# endregion
# ============================================================