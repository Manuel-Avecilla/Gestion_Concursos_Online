# Gestión de Sesiones, Usuarios y Permisos

Este documento detalla la implementación técnica de la gestión de usuarios, sesiones y permisos en la aplicación **Gestion_Concursos_Online**.

---

## 1. Tipos de Usuario

La aplicación extiende el modelo de usuario base de Django mediante una estrategia de **OneToOneField** para diferenciar roles específicos.

### Modelo Base: `Usuario`
Hereda de `AbstractUser` e incluye un campo discriminador:
- `rol`: Entero positivo que identifica el tipo de usuario (1: Administrador, 2: Participante, 3: Jurado, 4: Usuario).

### Perfiles Específicos
Existen modelos dedicados para cada rol principal, vinculados uno a uno con `Usuario`:
- **Participante**: Incluye alias, edad, nivel y puntuación.
- **Jurado**: Incluye experiencia, especialidad, disponibilidad y reputación.
- **Administrador**: Incluye área responsable, horario y estado.
- **Perfil**: Modelo base complementario para todos los usuarios con información común (foto, biografía).

> **Nota**: Tal como se indica en el `README.md` del proyecto, estos son los roles que definen el acceso a las distintas funcionalidades del sistema.

---

## 2. Control de Permisos y Autenticación

El control de acceso se realiza de manera estricta en tres niveles: Vistas, Templates y Formularios.

### En Vistas
Se utiliza el decorador `@permission_required` para restringir el acceso a las vistas según los permisos del usuario. Si el usuario no tiene los permisos necesarios, se lanza una excepción.

*Ejemplo:*
```python
@permission_required('Concursos_Online.view_concurso', raise_exception=True)
def dame_concurso(request, id_concurso):
    # Lógica de la vista
```

### En Templates
Se valida `request.user.is_authenticated` para mostrar opciones de login/registro o menú de usuario. Además, se verifica la existencia de perfiles asociados para renderizar enlaces específicos.

*Ejemplo en `_header.html`:*
```html
{% if not request.user.is_authenticated %}
    <!-- Enlaces de Login/Registro -->
{% else %}
    <!-- Menú de Usuario y Logout -->
{% endif %}
```

### En Formularios
Los formularios de creación y edición validan internamente que los datos correspondan al contexto del usuario, o son procesados por vistas que aseguran la integridad, asignando automáticamente el usuario logueado como responsable o autor.

---

## 3. Variables de Sesión

Para persistencia de datos relevantes durante la navegación, se almacenan 4 variables en la sesión del usuario (`request.session`) al momento de hacer **Login** o **Registro**.

### Variables Implementadas:
1.  **`usuario`**: Nombre de usuario (`username`).
2.  **`grupos`**: Lista de grupos a los que pertenece el usuario (formato string).
3.  **`hora_login`**: Fecha y hora del inicio de sesión.
4.  **`email`**: Correo electrónico del usuario.

### Comportamiento:
- **Visualización**: Estas variables se muestran permanentemente en la cabecera (`header`) de todas las páginas mientras el usuario está autenticado.
- **Ciclo de vida**: Se crean en el login/registro y se eliminan automáticamente al ejecutar el **Logout**.

---

## 4. Registro y Autenticación

### Registro de Usuarios (Sign Up)
Existen vistas diferenciadas para registrar cada tipo de usuario (`registrar_usuario`, `registrar_participante`, `registrar_jurado`).
- **Validaciones**: Se verifica que el formulario sea válido. Si el usuario ya está logueado, se redirige.
- **Lógica**: Se crea el `Usuario`, el `Perfil` y el modelo específico (`Participante`/`Jurado`).
- **Asignación de Grupos**: Se añade el usuario automáticamente a los grupos de permisos correspondientes (ej. 'Usuario', 'Participantes', 'Jurados').
- **Inicio de Sesión Automático**: Tras el registro exitoso, se loguea al usuario y se inicializan las variables de sesión.

### Login y Logout
- **Login**: Implementado mediante una vista personalizada (`MiLoginView`) que extiende `LoginView`. Se sobrescribe `form_valid` para inyectar las variables de sesión mencionadas anteriormente.
- **Logout**: Utiliza la vista estándar de Django, lo que limpia la sesión y elimina las variables almacenadas.

---

## 5. Formularios Dinámicos y Filtrados

La aplicación adapta el contenido de los formularios según el usuario que los consulta.

### Campos Dinámicos (ManyToMany/ForeignKeys)
En el formulario de búsqueda avanzada de perfiles (`PerfilBuscarAvanzada`), el campo de selección de usuarios (`ModelMultipleChoiceField`) varía sus opciones según el rol del usuario logueado:
- **Administradores**: Ven todos los perfiles.
- **Jurados**: Ven Jurados, Participantes y Usuarios estándar.
- **Participantes/Usuarios**: Solo ven Participantes y Usuarios estándar.

Esta lógica se implementa sobrescribiendo el método `__init__` del formulario y accediendo a `request.user`:

```python
def __init__(self, *args, **kwargs):
    self.request = kwargs.pop("request", None)
    super().__init__(*args, **kwargs)
    if self.request.user.rol == 1:
        # QuerySet completo para admins
```

### Asignación Automática en Creación
En los formularios de creación (como `concurso_create`), el usuario no selecciona el autor. Este se asigna automáticamente en la vista utilizando el usuario de la sesión (`request.user`).

```python
concurso.creador = usuario.administrador
```

### Búsqueda Filtrada
El formulario de búsqueda avanzada de perfiles actúa también como un filtro de contenido dependiente del usuario logueado, restringiendo los resultados a los que el usuario tiene permiso de ver (como se detalló en la sección de campos dinámicos).

---

## 6. Reinicio de Contraseña

> **Estado**: 🚧 No implementado.

Actualmente, la funcionalidad de recuperación de contraseña no está desarrollada en la interfaz web.
**Nota técnica**: Django ofrece mecanismos nativos para simular el flujo de recuperación de contraseña en entorno local (imprimiendo el enlace en consola), pero esta característica no ha sido integrada en el proyecto actual.

---

## 7. Consideraciones Importantes

### Fixtures y Grupos de Permisos
Para el correcto funcionamiento de la aplicación, especialmente en lo referente a la asignación de roles y permisos, es **imprescindible** que la base de datos esté poblada con los grupos de seguridad definidos.

Al cargar los datos iniciales (fixtures), asegúrese de incluir los **Grupos** y **Permisos**, ya que la lógica de registro y control de acceso depende de su existencia previa.