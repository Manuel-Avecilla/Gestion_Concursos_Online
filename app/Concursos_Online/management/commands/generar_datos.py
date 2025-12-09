# ============================================================
# region Importaciones
# ============================================================

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone
from Concursos_Online.models import *

# endregion
# ============================================================


# python manage.py migrate          <-- Comando para generar la base de datos
# python manage.py generar_grupos   <-- Comando para generar los grupos y permisos
# python manage.py generar_datos    <-- Comando para generar los datos y rellenar la base de datos

# python manage.py dumpdata --indent 4 > Concursos_Online/fixtures/datos.json   <-- Comando para guardar los datos


class Command(BaseCommand):
    help = 'Generando datos usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')  # Faker en español

        # region Creación de Usuarios
        # ------------------------------------------------------------
        # 1. Se crea una lista vacía `usuarios` para guardar las instancias creadas.
        # 2. Se generan 30 usuarios falsos con datos de Faker:
        #    - username: nombre de usuario único.
        #    - email: email único.
        #    - password: contraseña aleatoria de 10 caracteres.
        # 3. Cada usuario creado se guarda en la lista `usuarios` para usarlos después.
        # ------------------------------------------------------------
        
        self.stdout.write("Generando usuarios...")
        usuarios = []
        u_grupo_usuarios, _ = Group.objects.get_or_create(name="Usuario")
        
        for _ in range(30):
            
            user = Usuario.objects.create_user(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password="iespsur.25"
            )
            u_grupo_usuarios.user_set.add(user)
            usuarios.append(user)


        
        # endregion

        # region Creación de Perfiles
        # ------------------------------------------------------------
        # 1. Se recorre la lista de usuarios creada anteriormente.
        # 2. Por cada usuario se genera un perfil asociado (relación 1:1).
        # 3. Faker rellena los campos del perfil:
        #    - nombre_completo, biografía, fecha de nacimiento e imagen.
        # ------------------------------------------------------------
        
        self.stdout.write("Generando perfiles...")
        contador = 0

        for usuario in usuarios:
            contador += 1
            num = str(contador).zfill(3)  # → 001, 002, 003 ... 060

            Perfil.objects.create(
                usuario=usuario,
                nombre_completo=fake.name(),
                biografia=fake.text(200),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=70),
                imagen_perfil=f"usuarios/foto-perfil-{num}.jpg"
            )
    
        # endregion

        # region Creación de Administradores
        # ------------------------------------------------------------
        # 1. Se eligen 3 usuarios al azar para ser administradores.
        # 2. Por cada usuario seleccionado se crea un objeto Administrador (relación 1:1).
        # 3. Faker genera datos del área y horario de trabajo.
        # ------------------------------------------------------------
        
        self.stdout.write("Generando administradores...")
        administradores = []
        for u in random.sample(usuarios, 3):
            
            u.rol = Usuario.ADMINISTRADOR
            u.save()
            grupo_admin = Group.objects.get(name="Administrador")
            grupo_admin.user_set.add(u)
            
            administradores.append(Administrador.objects.create(
                usuario=u,
                area_responsable=fake.job(),
                activo=True,
                horario_disponible=fake.time()
            ))
        
        # endregion

        # region Creación de Jurados
        # ------------------------------------------------------------
        # 1. Se eligen 5 usuarios distintos que no sean administradores.
        # 2. Por cada usuario seleccionado se crea un objeto Jurado (relación 1:1).
        # 3. Faker y random generan la experiencia, especialidad y puntuación media.
        # ------------------------------------------------------------
        self.stdout.write("Generando jurados...")
        
        # 1. Obtener los usuarios que ya son administradores
        usuarios_admin = [admin.usuario for admin in administradores]
        
        # 2. Filtrar los usuarios que NO están en la lista anterior
        usuarios_disponibles = []
        for usuario in usuarios:
            if usuario not in usuarios_admin:
                usuarios_disponibles.append(usuario)
        
        # 3. Seleccionar 5 usuarios al azar de los disponibles
        usuarios_para_jurado = random.sample(usuarios_disponibles, 5)
        
        # 4. Crear los objetos Jurado asociados a esos usuarios
        jurados = []
        for u in usuarios_para_jurado:
            
            u.rol = Usuario.JURADO
            u.save()
            grupo_jurado = Group.objects.get(name="Jurados")
            grupo_jurado.user_set.add(u)
            
            nuevo_jurado = Jurado.objects.create(
                usuario=u,
                experiencia=random.randint(1, 10),
                especialidad=fake.job(),
                disponible=True,
                puntuacion_media=round(random.uniform(3, 10), 2)
            )
            jurados.append(nuevo_jurado)
        
        # endregion

        # region Creación de Participantes
        # ------------------------------------------------------------
        self.stdout.write("Generando participantes...")
        
        # 1. Obtener los usuarios que ya son administradores o jurados
        usuarios_admin = [admin.usuario for admin in administradores]
        usuarios_jurado = [jurado.usuario for jurado in jurados]

        # 2. Filtrar los usuarios que NO están en esas listas (usuarios libres)
        usuarios_disponibles = []
        for usuario in usuarios:
            if usuario not in usuarios_admin and usuario not in usuarios_jurado:
                usuarios_disponibles.append(usuario)

        # 3. Seleccionar 10 usuarios al azar de los disponibles
        usuarios_para_participantes = random.sample(usuarios_disponibles, 10)

        # 4. Crear los objetos Participante asociados a esos usuarios
        participantes = []
        for u in usuarios_para_participantes:
            
            u.rol = Usuario.PARTICIPANTE
            u.save()
            grupo_participante = Group.objects.get(name="Participantes")
            grupo_participante.user_set.add(u)
            
            nuevo_participante = Participante.objects.create(
                usuario=u,
                alias=fake.user_name(),
                edad=random.randint(18, 60),
                nivel=random.randint(1, 5),
                puntuacion_total=round(random.uniform(0, 100), 2) # Una puntuación decimal entre 0 y 100 con 2 decimales.
            )
            participantes.append(nuevo_participante)
        # endregion

        # region Creación de Concursos
        # ------------------------------------------------------------
        self.stdout.write("Generando concursos...")
        # 1. Creamos una lista vacía para guardar los concursos
        concursos = []
        # 2. Creamos 7 concursos
        for i in range(7):
            # Elegir un administrador al azar como creador
            creador = random.choice(administradores)
            
            # Generar fechas de inicio y final de forma consistente
            fecha_inicio = timezone.now() - timedelta(days=random.randint(10, 200))
            fecha_final = fecha_inicio + timedelta(days=random.randint(5, 15))
            
            # Crear el concurso
            estadoBolean = False
            estado = random.randint(0, 1)
            if (estado == 0):
                estadoBolean = False
            else:
                estadoBolean = True
            
            concurso = Concurso.objects.create(
                nombre = f"{random.choice(['Concurso','Festival','Premio','Torneo'])} {random.choice(['Nacional','Creativo','Juvenil','Internacional','Regional'])} de {random.choice(['Fotografía','Arte Digital','Robótica','Pintura','Canto','Ciencia'])}",
                descripcion=fake.text(300),
                fecha_inicio=fecha_inicio,
                fecha_final=fecha_final,
                activo=estadoBolean,
                creador=creador
            )
            
            # Guardar en la lista para usarlo después (trabajos, inscripciones, jurados)
            concursos.append(concurso)
        # endregion

        # region Asignando Jurados a Concursos (N:N)
        # ------------------------------------------------------------
        self.stdout.write("Asignando Jurados a Concursos...")
        # 1. Recorremos todos los jurados
        for jurado in jurados:
            # 2. Seleccionamos 2 concursos al azar para cada jurado
            concursos_asignados = random.sample(concursos, k=2)
            # 3. Creamos la relación en el modelo intermedio Asigna
            for concurso in concursos_asignados:
                Asigna.objects.create(
                    jurado=jurado,
                    concurso=concurso,
                    activo=True
                )
        # endregion

        # region Inscribiendo Participantes en Concursos (N:N)
        # ------------------------------------------------------------
        self.stdout.write("Inscribiendo Participantes en Concursos...")
        # 1. Recorremos todos los participantes
        for participante in participantes:
            # 2. Seleccionamos 2 concursos al azar para cada participante
            concursos_inscritos = random.sample(concursos, k=2)
            
            # 3. Creamos la relación en el modelo intermedio Inscribe
            for concurso in concursos_inscritos:
                Inscribe.objects.create(
                    participante=participante,
                    concurso=concurso,
                    fecha_inscripcion=timezone.now()
                )
        # endregion

        # region Creando Trabajos (1:N con Participante y Concurso)
        # ------------------------------------------------------------
        self.stdout.write("Creando Trabajos...")
        # 1. Creamos una lista vacía para guardar los trabajos
        trabajos = []
        
        # 2. Recorremos todos los participantes
        for participante in participantes:
            # 3. Seleccionamos 1 concurso al azar donde el participante esté inscrito
            concursos_participante = [inscribe.concurso for inscribe in participante.inscribe_participante.all()]
            if not concursos_participante:
                continue  # saltar si el participante no está inscrito en ningún concurso
            concurso = random.choice(concursos_participante)
            
            # 4. Crear el trabajo
            trabajo = Trabajo.objects.create(
                participante=participante,
                concurso=concurso,
                titulo=fake.sentence(nb_words=4), # frase aleatoria de 4 palabras
                descripcion=fake.text(150),
                archivo=fake.file_name(extension='pdf'),
                fecha_envio=timezone.now(),
                puntuacion_promedio=round(random.uniform(0, 10), 2)
            )
            
            # 5. Guardar en la lista para usar después en Evaluaciones
            trabajos.append(trabajo)
        # endregion

        # region Creando Evaluaciones (N:N con Jurado y Trabajo)
        # ------------------------------------------------------------
        self.stdout.write("Creando Evaluaciones...")
        # 1. Recorremos todos los trabajos
        for trabajo in trabajos:
            # 2. Obtenemos los jurados asignados al concurso del trabajo
            jurados_concurso = trabajo.concurso.jurados.all()

            # 3. Cada jurado del concurso evalúa el trabajo
            for jurado in jurados_concurso:
                Evaluacion.objects.create(
                    jurado=jurado,
                    trabajo=trabajo,
                    puntuacion=round(random.uniform(0, 10), 2),
                    comentario=fake.text(100),
                    fecha_evaluacion=timezone.now()
                )
        # endregion

        # region Creando Notificaciones (Administrador → Usuarios)
        # ------------------------------------------------------------
        self.stdout.write("Creando Notificaciones...")
        # 1. Recorremos todos los administradores
        for admin in administradores:
            # 2. Cada administrador envía 2 notificaciones
            for i in range(2):
                notificacion = Notificacion.objects.create(
                    autor=admin,
                    titulo=fake.sentence(nb_words=5),
                    mensaje=fake.text(150),
                    fecha_envio=timezone.now()
                )
                # 3. Elegir aleatoriamente 5 usuarios para recibir la notificación
                usuarios_receptores = random.sample(usuarios, 5)
                
                # 4. Crear las relaciones N:N usando el modelo intermedio Recibe
                for usuario in usuarios_receptores:
                    Recibe.objects.create(
                        usuario=usuario,
                        notificacion=notificacion,
                        estado=random.choice(['PE', 'EN']),
                        fecha_recepcion=timezone.now()
                    )
        # endregion
        
        # region Asignando ganadores a los concursos (1:N)
        self.stdout.write("Asignando ganadores a los concursos...")
        for concurso in concursos:
            # Obtenemos los participantes inscritos en ese concurso
            participantes_inscritos = [inscripcion.participante for inscripcion in concurso.inscribe_concurso.all()]

            # Si hay participantes, elegimos uno al azar como ganador
            if participantes_inscritos:
                ganador = random.choice(participantes_inscritos)
                concurso.ganador = ganador
                concurso.save()
        # endregion

        # region Creación de usuarios de PRUEBAS (super-admin, admin, jurado, participante)
        self.stdout.write("Creando usuarios de PRUEBAS...")

        

        User = get_user_model()

        up_grupo_admin, _ = Group.objects.get_or_create(name="Administrador")
        up_grupo_jurado, _ = Group.objects.get_or_create(name="Jurados")
        up_grupo_participante, _ = Group.objects.get_or_create(name="Participantes")
        up_grupo_usuario, _ = Group.objects.get_or_create(name="Usuario")  # Rol general

        usuarios_base = {
            "super-admin": {"is_superuser": True, "groups": []},
            "admin": {"is_superuser": False, "groups": [up_grupo_admin]},
            "jurado": {"is_superuser": False, "groups": [up_grupo_jurado]},
            "participante": {"is_superuser": False, "groups": [up_grupo_participante]},
        }

        for username, datos in usuarios_base.items():
            # Si ya existe, eliminarlo
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()

            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="1234"
            )

            # Asignar rol general "Usuario"
            user.groups.add(up_grupo_usuario)

            # Si es superadmin
            if datos["is_superuser"]:
                user.is_superuser = True
                user.is_staff = True
                user.save()
            else:
                # Asignar su grupo específico
                for g in datos["groups"]:
                    user.groups.add(g)

            self.stdout.write(f"Usuario creado: {username} / 1234")

        # endregion

        self.stdout.write(self.style.SUCCESS("Datos generados correctamente."))