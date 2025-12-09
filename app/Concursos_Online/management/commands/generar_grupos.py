# ============================================================
# region Importaciones
# ============================================================

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

# endregion
# ============================================================


# python manage.py migrate          <-- Comando para generar la base de datos
# python manage.py generar_grupos   <-- Comando para generar los grupos y permisos
# python manage.py generar_datos    <-- Comando para generar los datos y rellenar la base de datos

# python manage.py dumpdata --indent 4 > Concursos_Online/fixtures/datos.json   <-- Comando para guardar los datos


class Command(BaseCommand):
    help = "Crea los grupos y asigna los permisos necesarios."

    def handle(self, *args, **kwargs):

        self.stdout.write("Creando grupos...")

        # Diccionario con los grupos y sus permisos
        grupos = {
            # ______________________ GRUPO ADMINISTRADOR _______________________________
            "Administrador": [
                # Administrador
                "add_administrador", "change_administrador", "delete_administrador", "view_administrador",

                # Usuario
                "add_usuario", "change_usuario", "delete_usuario", "view_usuario",

                # Perfil
                "add_perfil", "change_perfil", "delete_perfil", "view_perfil",

                # Participante
                "add_participante", "change_participante", "delete_participante", "view_participante",

                # Jurado
                "add_jurado", "change_jurado", "delete_jurado", "view_jurado",

                # Concurso
                "add_concurso", "change_concurso", "delete_concurso", "view_concurso",

                # Trabajo
                "add_trabajo", "change_trabajo", "delete_trabajo", "view_trabajo",

                # Evaluación
                "add_evaluacion", "change_evaluacion", "delete_evaluacion", "view_evaluacion",

                # Inscripciones
                "add_inscribe", "change_inscribe", "delete_inscribe", "view_inscribe",

                # Notificaciones
                "add_notificacion", "change_notificacion", "delete_notificacion", "view_notificacion",

                # Asignaciones
                "add_asigna", "change_asigna", "delete_asigna", "view_asigna",

                # Recibe
                "add_recibe", "change_recibe", "delete_recibe", "view_recibe",
            ],

            # ______________________ GRUPO JURADO ______________________________________
            "Jurados": [
                # Concurso
                "view_concurso",

                # Participante
                "view_participante",
                
                # Jurado
                "view_jurado",
                
                # Trabajo
                "view_trabajo",

                # Evaluación
                "add_evaluacion", "change_evaluacion", "view_evaluacion",

                # Notificaciones
                "view_notificacion",
                
                # Asignaciones
                "view_asigna",
                
                # Inscripciones
                "view_inscribe",
                
            ],

            # ______________________ GRUPO PARTICIPANTE ________________________________
            "Participantes": [
                # Concurso
                "view_concurso",

                # Trabajo
                "add_trabajo", "view_trabajo",

                # Inscripciones
                "add_inscribe", "change_inscribe", "view_inscribe",

                # Notificaciones
                "view_notificacion",

                # Participante
                "view_participante",

                # Perfil
                "view_perfil",
            ],
            
            # ______________________ GRUPO USUARIO ________________________________
            "Usuario": [
                # Concurso
                "view_concurso",

                # Participante
                "view_participante",

                # Perfil
                "view_perfil",
                
                # Notificaciones
                "view_notificacion",
            ],
        }

        for nombre_grupo, permisos in grupos.items():

            grupo, creado = Group.objects.get_or_create(name=nombre_grupo)

            if creado:
                self.stdout.write(f"Grupo creado: {nombre_grupo}")
            else:
                self.stdout.write(f"Grupo ya existia: {nombre_grupo}")

            # Agregar permisos
            for codename in permisos:
                try:
                    permiso = Permission.objects.get(codename=codename)
                    grupo.permissions.add(permiso)
                    
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"Permiso no encontrado: {codename}")
                    )

        self.stdout.write(self.style.SUCCESS("Grupos creados y actualizados correctamente."))

        """
        
        #Para ver todos los permisos disponibles por consola:
        
        self.stdout.write("\nPermisos disponibles en la app:\n")
        app_label = "Concursos_Online"
        content_types = ContentType.objects.filter(app_label=app_label)
        permisos_app = Permission.objects.filter(content_type__in=content_types)
        for p in permisos_app:
            self.stdout.write(f"- {p.codename}   ({p.name})")
        self.stdout.write(self.style.SUCCESS("\nListado completo de permisos mostrado con exito."))
        
        """