# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render
from Concursos_Online.models import *

# endregion
# ============================================================


# ============================================================
# region Errores personalizados (400, 403, 404, 500)
# ============================================================

def mi_error_404(request,exception=None):
    return render(request,'error/404.html',None,None,404)

def mi_error_403(request,exception=None):
    return render(request,'error/403.html',None,None,403)

def mi_error_400(request,exception=None):
    return render(request,'error/400.html',None,None,400)

def mi_error_500(request,exception=None):
    return render(request,'error/500.html',None,None,500)

# endregion
# ============================================================