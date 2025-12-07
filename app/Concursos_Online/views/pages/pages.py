# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render

# endregion
# ============================================================




# ============================================================
# region Páginas públicas (Home, Menu)
# ============================================================

def home(request):
    return render(request, 'pages/home.html')

def menu(request):
    return render(request, 'pages/menu.html')

# endregion
# ============================================================