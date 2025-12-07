# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render
from Concursos_Online.models import Administrador
from Concursos_Online.forms import AdministradorForm, AdministradorBuscarAvanzada
from django.contrib.auth.decorators import permission_required

from django.contrib import messages
from django.shortcuts import redirect

# endregion
# ============================================================