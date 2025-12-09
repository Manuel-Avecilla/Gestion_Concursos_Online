# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from Concursos_Online.models import Usuario, Participante, Jurado, Perfil
from Concursos_Online.forms import RegistroUsuarioForm, RegistroParticipanteForm, RegistroJuradoForm

from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from django.utils import timezone
from django.contrib.auth.models import Group

# endregion
# ============================================================




# ============================================================
# region Registro
# ============================================================

def pagina_registro(request):
    return render(request, 'registration/page_signup.html')


def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        
        if formulario.is_valid():
            
            user = formulario.save()
            
            perfil = Perfil.objects.create(usuario = user)
            perfil.save()
            grupo_usuario = Group.objects.get(name='Usuario')
            grupo_usuario.user_set.add(user)
            
            login(request, user)
            
            # 4 variables Sesion ----------------------------------
            
            # Nombre Usuario
            request.session['usuario'] = user.username
            
            # Grupo
            u_grupos = ", ".join(user.groups.values_list('name', flat=True))
            request.session['grupos'] = u_grupos
            
            # Hora Login
            request.session['hora_login'] = timezone.now().strftime("%d/%m/%Y %H:%M")
            
            # Email
            request.session['email'] = user.email
            
            #-------------------------------------------------------
            
            return redirect('home')
    else:
        formulario = RegistroUsuarioForm()
        
    return render(request, 'registration/signup_usuario.html', {'formulario': formulario})


def registrar_participante(request):
    if request.method == 'POST':
        formulario = RegistroParticipanteForm(request.POST)
        
        if formulario.is_valid():
            
            user = formulario.save()
            
            perfil = Perfil.objects.create(usuario = user)
            perfil.save()
            grupo_usuario = Group.objects.get(name='Usuario')
            grupo_usuario.user_set.add(user)
            
            grupo = Group.objects.get(name='Participantes')
            grupo.user_set.add(user)
            
            participante = Participante.objects.create(
                usuario = user,
                alias = formulario.cleaned_data.get('alias'),
                edad = formulario.cleaned_data.get('edad'),
                )
            participante.save()
            
            login(request, user)
            
            # 4 variables Sesion ----------------------------------
            
            # Nombre Usuario
            request.session['usuario'] = user.username
            
            # Grupo
            u_grupos = ", ".join(user.groups.values_list('name', flat=True))
            request.session['grupos'] = u_grupos
            
            # Hora Login
            request.session['hora_login'] = timezone.now().strftime("%d/%m/%Y %H:%M")
            
            # Email
            request.session['email'] = user.email
            
            #-------------------------------------------------------
            
            return redirect('home')
    else:
        formulario = RegistroParticipanteForm()
        
    return render(request, 'registration/signup_participante.html', {'formulario': formulario})


def registrar_jurado(request):
    if request.method == 'POST':
        formulario = RegistroJuradoForm(request.POST)
        
        if formulario.is_valid():
            
            user = formulario.save()
            
            perfil = Perfil.objects.create(usuario = user)
            perfil.save()
            grupo_usuario = Group.objects.get(name='Usuario')
            grupo_usuario.user_set.add(user)
            
            grupo = Group.objects.get(name='Jurados')
            grupo.user_set.add(user)
            
            jurado = Jurado.objects.create(
                usuario = user,
                experiencia=formulario.cleaned_data['experiencia'],
                disponible=formulario.cleaned_data['disponible'],
                )
            jurado.save()
            
            login(request, user)
            
            # 4 variables Sesion ----------------------------------
            
            # Nombre Usuario
            request.session['usuario'] = user.username
            
            # Grupo
            u_grupos = ", ".join(user.groups.values_list('name', flat=True))
            request.session['grupos'] = u_grupos
            
            # Hora Login
            request.session['hora_login'] = timezone.now().strftime("%d/%m/%Y %H:%M")
            
            # Email
            request.session['email'] = user.email
            
            #-------------------------------------------------------
            
            return redirect('home')
    else:
        formulario = RegistroJuradoForm()
        
    return render(request, 'registration/signup_jurado.html', {'formulario': formulario})


# endregion
# ============================================================




# ============================================================
# region Login
# ============================================================


class MiLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        
        # 4 variables Sesion -----------------------------------
        
        # Nombre Usuario
        self.request.session['usuario'] = user.username
        
        # Grupo
        u_grupos = ", ".join(user.groups.values_list('name', flat=True))
        self.request.session['grupos'] = u_grupos
        
        # Hora Login
        self.request.session['hora_login'] = timezone.now().strftime("%d/%m/%Y %H:%M")
        
        # Email
        self.request.session['email'] = user.email
        
        #-------------------------------------------------------

        return response


# endregion
# ============================================================