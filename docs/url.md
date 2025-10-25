# URLS del Sistema

A continuación se detallan las rutas (URLs) implementadas en el sistema **Django**.  
Cada apartado describe su función, los parámetros esperados y las relaciones entre modelos que utiliza.

## Índice de URLs

---

### `/concursos-online/listar/`
Lista todos los **concursos** con sus datos asociados.  
Incluye información relacionada, como participantes, creador y ganador.

---

### `/concursos-online/<int:id_concurso>`
Muestra el **detalle de un concurso** específico.  
Parámetro:  
- `id_concurso`: ID del concurso.  
Incluye información relacionada, como participantes, creador y ganador.

---

### `/concursos-online/<int:anyo_concurso>/<int:mes_concurso>/`
Lista todos los **concursos** con sus datos asociados, que comienzen en el mismo mes y año 
Parámetros:  
- `anyo_concurso`: Año de la fecha de inicio del concurso.
- `mes_concurso`: Mes de la fecha de inicio del concurso.  
Incluye información relacionada, como participantes, creador y ganador.

---

### `/concursos-online/listar/activo/<str:activo>/`
Lista de **concursos** con sus datos asociados:

Parámetros:  
- `activo`: Estado del concurso.  
- Si `activo` es "true" en la URL, solo ves los concursos activos.  
- Si `activo` es "false", ves todos los concursos (activos e inactivos).  
- Y siempre están ordenados por fecha de inicio.  
Incluye información relacionada, como participantes, creador y ganador.

---

### `/concursos-online/listar/texto/<str:texto>/`
Lista de **concursos** con sus datos asociados:

Parámetros:  
- `texto`: Texto que puede contener la descripcion del concurso.  
- Lista los concursos que contienen `texto` en su descripción.  
- Los concursos resultantes están ordenados de forma descendente (de Z a A) según el nombre.  
Incluye información relacionada, como participantes, creador y ganador.

---

### `/concursos-online/ultimo-participante-inscrito/<int:id_concurso>/`
Muestra el **detalle de un Participante** específico. 

Parámetros:  
- `id_concurso`: ID del concurso.  
- Una url que permite ver el participante que se inscribió más recientemente en un concurso concreto, utilizando el `id_concurso`.  
- Muestra únicamente la información de ese último inscrito, limitando la consulta a un solo registro.  
Incluye información del participante.

---

[⬅️ Volver al README principal](../README.md)