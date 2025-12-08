# ============================================================
# region Importaciones
# ============================================================

from django.urls import path
from . import views
from django.urls import re_path

# endregion
# ============================================================




urlpatterns = [
    
    # ============================================================
    # region URL Páginas públicas (Home, Menu)
    # ============================================================

    path('',views.home, name='home'),
    path('menu',views.menu, name='menu'),

    # endregion
    # ============================================================




    # ============================================================
    # region URL Sesiones
    # ============================================================

    path('registro',views.registrar_usuario,name='registrar_usuario'),

    # endregion
    # ============================================================




    # ============================================================
    # region URL Usuario
    # ============================================================

    #---------Detalles-Lista---------
    path('usuario/listar', views.usuarios_listar, name='usuarios_listar'),
    path('usuario/<int:id_usuario>', views.dame_usuario, name='dame_usuario'),

    #--------------CRUD--------------
    path('usuario/crear/',views.usuario_create, name='usuario_create'),
    path('usuario/buscar/',views.usuario_buscar, name='usuario_buscar'),
    path('usuario/buscar/avanzado/',views.usuario_buscar_avanzado, name='usuario_buscar_avanzado'),
    path('usuario/editar/<int:id_usuario>', views.usuario_editar, name="usuario_editar"),
    path('usuario/eliminar/<int:id_usuario>', views.usuario_eliminar, name="usuario_eliminar"),

    #-------------Filtros------------
    path('usuario/filtro/sin-notificaciones', views.usuarios_sin_notificar, name='usuarios_sin_notificar'),

    # endregion
    # ============================================================
    
    
    
    
    # ============================================================
    # region URL Perfil
    # ============================================================

    #---------Detalles-Lista---------
    path("usuario/perfil/listar",views.perfiles_listar, name="perfiles_listar"),
    path("usuario/perfil/<int:id_perfil>",views.dame_perfil, name="dame_perfil"),

    #--------------CRUD--------------
    path('usuario/perfil/crear/',views.perfil_create, name='perfil_create'),
    path('usuario/perfil/buscar/avanzado/',views.perfil_buscar_avanzado, name='perfil_buscar_avanzado'),
    path('usuario/perfil/editar/<int:id_perfil>', views.perfil_editar, name="perfil_editar"),
    path('usuario/perfil/eliminar/<int:id_perfil>', views.perfil_eliminar, name="perfil_eliminar"),

    #-------------Filtros------------

    # endregion
    # ============================================================
    
    
    
    
    # ============================================================
    # region URL Participante
    # ============================================================

    #---------Detalles-Lista---------
    path('usuario/participante/listar',views.participantes_listar, name='participantes_listar'),
    path('usuario/participante/<int:id_participante>',views.dame_participante, name='dame_participante'),

    #--------------CRUD--------------
    path('usuario/participante/crear/',views.participante_create, name='participante_create'),
    path('usuario/participante/buscar/avanzado/',views.participante_buscar_avanzado, name='participante_buscar_avanzado'),
    path('usuario/participante/editar/<int:id_participante>', views.participante_editar, name="participante_editar"),
    path('usuario/participante/eliminar/<int:id_participante>', views.participante_eliminar, name="participante_eliminar"),

    #-------------Filtros------------
    path('usuario/participante/filtro/concurso/<int:id_concurso>',views.dame_participantes_concurso, name='dame_participantes_concurso'),
    path('usuario/participante/filtro/ultimo-participante/concurso/<int:id_concurso>', views.dame_ultimo_participante, name='dame_ultimo_participante'),
    re_path(r'^usuario/participante/filtro/alias/(?P<alias_participante>[a-zA-Z0-9_-]+)/$', views.detalle_participante_alias, name='detalle_participante_alias'),
    # Explicacion re_path:
    # Patrón: ^usuario/participante/filtro/alias/CUALQUIER_CADENA/$.
    # ?P<alias_participante> Esto nombra la parte capturada como alias_participante
    # Si un usuario navega a http://127.0.0.1:8000/usuario/participante/filtro/alias/usuario_ejemplo123/
    # la cadena usuario_ejemplo123 será capturada como la variable alias_participante y pasada a la vista.

    # endregion
    # ============================================================
    
    
    
    
    # ============================================================
    # region URL Jurado
    # ============================================================

    #---------Detalles-Lista---------
    path('usuario/jurado/listar', views.jurados_listar, name='jurados_listar'),
    path('usuario/jurado/<int:id_jurado>', views.dame_jurado, name='dame_jurado'),

    #--------------CRUD--------------
    path('usuario/jurado/crear/',views.jurado_create, name='jurado_create'),
    path('usuario/jurado/buscar/avanzado/',views.jurado_buscar_avanzado, name='jurado_buscar_avanzado'),
    path('usuario/jurado/editar/<int:id_jurado>', views.jurado_editar, name="jurado_editar"),
    path('usuario/jurado/eliminar/<int:id_jurado>', views.jurado_eliminar, name="jurado_eliminar"),
    
    #-------------Filtros------------
    path('usuario/jurado/filtro/metricas_experiencia/', views.metricas_experiencia_jurados, name='metricas_experiencia_jurados'),

    # endregion
    # ============================================================
    
    
    
    
    # ============================================================
    # region URL Administrador
    # ============================================================

    #---------Detalles-Lista---------
    path("usuario/administrador/listar",views.administradores_listar, name="administradores_listar"),
    path("usuario/administrador/<int:id_administrador>",views.dame_administrador, name="dame_administrador"),

    #--------------CRUD--------------
    path('usuario/administrador/crear/',views.administrador_create, name='administrador_create'),
    path('usuario/administrador/buscar/avanzado/',views.administrador_buscar_avanzado, name='administrador_buscar_avanzado'),
    path('usuario/administrador/editar/<int:id_administrador>', views.administrador_editar, name="administrador_editar"),
    path('usuario/administrador/eliminar/<int:id_administrador>', views.administrador_eliminar, name="administrador_eliminar"),

    # endregion
    # ============================================================
    
    
    
    
    # ============================================================
    # region URL Concurso
    # ============================================================

    #---------Detalles-Lista---------
    path('concurso/listar', views.concursos_listar, name='concursos_listar'),
    path('concurso/<int:id_concurso>', views.dame_concurso, name='dame_concurso'),

    #--------------CRUD--------------
    path('concurso/crear/',views.concurso_create, name='concurso_create'),
    path('concurso/buscar/avanzado/',views.concurso_buscar_avanzado, name='concurso_buscar_avanzado'),
    path('concurso/editar/<int:id_concurso>', views.concurso_editar, name="concurso_editar"),
    path('concurso/eliminar/<int:id_concurso>', views.concurso_eliminar, name="concurso_eliminar"),

    #-------------Filtros------------
    path('concurso/filtro/<int:anyo_concurso>/<int:mes_concurso>', views.dame_concursos_fecha, name='dame_concursos_fecha'),
    path('concurso/filtro/listar/activo/<str:activo>', views.dame_concurso_activo, name='dame_concurso_activo'),
    path('concurso/filtro/listar/texto/<str:texto>', views.dame_concurso_texto, name='dame_concurso_texto'),

    # endregion
    # ============================================================
    
]
