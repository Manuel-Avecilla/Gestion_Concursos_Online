# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from Concursos_Online.models import Usuario, Participante, Jurado, Perfil
from Concursos_Online.forms import RegistroForm

from django.contrib.auth import login
from django.contrib.auth.models import Group

# endregion
# ============================================================




# ============================================================
# region Autenticación y Registro
# ============================================================

def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        
        if formulario.is_valid():
            
            user = formulario.save()
            
            perfil = Perfil.objects.create(usuario = user)
            perfil.save()
            
            rol = int(formulario.cleaned_data.get('rol'))
            
            if(rol == Usuario.PARTICIPANTE):
                
                grupo = Group.objects.get(name='Participantes')
                grupo.user_set.add(user)
                
                participante = Participante.objects.create(usuario = user)
                participante.save()
                
            elif(rol == Usuario.JURADO):
                
                grupo = Group.objects.get(name='Jurados')
                grupo.user_set.add(user)
                
                jurado = Jurado.objects.create(usuario = user)
                jurado.save()
            
            login(request, user)
            
            return redirect('home')
    else:
        formulario = RegistroForm()
        
    return render(request, 'registration/signup.html', {'formulario': formulario})

# endregion
# ============================================================