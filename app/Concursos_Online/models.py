from django.db import models

#------------------------------- USUARIO ------------------------------------------
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=100) 
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_usuario

#------------------------------- PERFIL ------------------------------------------
class Perfil(models.Model):
    # Relacion 1:1 con Usuario (Tiene)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    
    nombre_completo = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    imagen_perfil = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.nombre_usuario}"

#------------------------------- JURADO ------------------------------------------
class Jurado(models.Model):
    # Relacion 1:1 con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='jurado')
    
    experiencia = models.PositiveIntegerField(default=0)
    especialidad = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    puntuacion_media = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Relacion N:N con Concursos (Asigna)
    concursos = models.ManyToManyField('Concurso', through='Asigna', related_name='jurados')

    def __str__(self):
        return f"Jurado: {self.usuario.nombre_usuario}"

#------------------------------- PARTICIPANTE ------------------------------------------
class Participante(models.Model):
    # Relacion 1:1 con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='participante')
    
    alias = models.CharField(max_length=50, unique=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    nivel = models.PositiveIntegerField(default=1)
    puntuacion_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Participante: {self.alias}"

#------------------------------- ADMINISTRADOR ------------------------------------------
class Administrador(models.Model):
    # Relacion 1:1 con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrador')
    
    area_responsable = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    horario_disponible = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Administrador: {self.usuario.nombre_usuario}"

#------------------------------- NOTIFICACION ------------------------------------------
class Notificacion(models.Model):
    # Relacion 1:N con Administrador (Envia)
    autor = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='notificaciones_enviadas')
    # Relacion N:N con Usuario (Recibe)
    usuarios = models.ManyToManyField(Usuario, through='Recibe', related_name='notificaciones_recibidas')

    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

#------------------------------- RECIBE (Relacion) ------------------------------------------
class Recibe(models.Model):
    ESTADOS = [('PE', 'Pendiente'), ('EN', 'Enviada')]
    
    # FK de la relacion N:N con Usuario - Notificacion
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recibos')
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, related_name='recibos')
    
    estado = models.CharField(max_length=2, choices=ESTADOS, default='PE')
    fecha_recepcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre_usuario} recibe {self.notificacion.titulo}"

#------------------------------- CONCURSO ------------------------------------------
class Concurso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    activo = models.BooleanField(default=True)

    # Relacion 1:N con Administrador (Crea)
    creador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='concursos_creados')
    # Relacion 1:N con Participante (Gana)
    ganador = models.ForeignKey(Participante, on_delete=models.SET_NULL, null=True, blank=True, related_name='concursos_ganados')
    # Relacion N:N con Participante (Inscribe)
    participantes = models.ManyToManyField(Participante, through='Inscribe', related_name='inscritos')

    def __str__(self):
        return self.nombre

#------------------------------- TRABAJO ------------------------------------------
class Trabajo(models.Model):
    # Relacion 1:N con Participante (Realiza)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='trabajo_participante')
    # Relacion 1:N con Concurso (Pertenece)
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name='trabajo_concurso')
    # Relacion N:N con Jurado (Evaluacion)
    jurados = models.ManyToManyField(Jurado, through='Evaluacion', related_name='trabajos_evaluados')

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    archivo = models.CharField(max_length=200,blank=True, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    puntuacion_promedio = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.titulo} ({self.participante.alias})"

#------------------------------- INSCRIBE (Relacion) ------------------------------------------
class Inscribe(models.Model):
    # FK de la relacion N:N con Participante - Concurso
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='inscribe_participante')
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name='inscribe_concurso')
    
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participante.alias} inscrito en {self.concurso.nombre}"

#------------------------------- ASIGNA (Relacion) ------------------------------------------
class Asigna(models.Model):
    # FK de la relacion N:N con Jurado - Concurso
    jurado = models.ForeignKey(Jurado, on_delete=models.CASCADE, related_name='asigna_jurado')
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name='asigna_concurso')
    
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.jurado} asignado a {self.concurso}"

#------------------------------- EVALUACION (Relacion) ------------------------------------------
class Evaluacion(models.Model):
    # FK de la relacion N:N con Jurado - Trabajo
    jurado = models.ForeignKey(Jurado, on_delete=models.CASCADE, related_name='evaluacion_jurado')
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='evaluacion_trabajo')
    
    puntuacion = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    comentario = models.TextField(blank=True, null=True)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jurado.usuario.nombre_usuario} evalúa {self.trabajo.titulo}"
