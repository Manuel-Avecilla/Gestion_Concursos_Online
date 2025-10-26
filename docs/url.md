# URLS del Sistema

A continuación se detallan las rutas (URLs) implementadas en el sistema **Django**.  
Cada apartado describe su función, los parámetros esperados y las relaciones entre modelos que utiliza.

## Índice de URLs

---

### 1. `/concursos-online/listar/`
Lista todos los **concursos** con sus datos asociados.  
Incluye información relacionada, como participantes, creador y ganador.

---

### 2. `/concursos-online/<int:id_concurso>`
Muestra el **detalle de un concurso** específico.  
Incluye información relacionada, como participantes, creador y ganador.

Parámetro:  

- `id_concurso`: ID del concurso.  

---

### 3. `/concursos-online/<int:anyo_concurso>/<int:mes_concurso>/`
Lista todos los **concursos** con sus datos asociados, que comienzen en el mismo mes y año
Incluye información relacionada, como participantes, creador y ganador.

Parámetros:  

- `anyo_concurso`: Año de la fecha de inicio del concurso.
- `mes_concurso`: Mes de la fecha de inicio del concurso.  

---

### 4. `/concursos-online/listar/activo/<str:activo>/`
Lista de **concursos** con sus datos asociados:
Incluye información relacionada, como participantes, creador y ganador.
Y siempre están ordenados por fecha de inicio. 

Parámetros:  

- `activo`: Estado del concurso.  
- Si `activo` es "true" en la URL, solo ves los concursos activos.  
- Si `activo` es "false", ves todos los concursos (activos e inactivos).  

---

### 5. `/concursos-online/listar/texto/<str:texto>/`
Lista de **concursos** con sus datos asociados:
Incluye información relacionada, como participantes, creador y ganador.
Los concursos resultantes están ordenados de forma descendente (de Z a A) según el nombre.

Parámetros:

- `texto`: Texto que puede contener la descripcion del concurso.  
- Lista los concursos que contienen `texto` en su descripción.    

---

### 6. `/concursos-online/ultimo-participante-inscrito/<int:id_concurso>/`
Muestra el **detalle de un Participante** específico. 
Incluye información del participante.
Muestra únicamente la información de ese último inscrito, limitando la consulta a un solo registro.

Parámetros:

- `id_concurso`: ID del concurso.  
- Una url que permite ver el participante que se inscribió más recientemente en un concurso concreto, utilizando el `id_concurso`.  

---

### 7. `re_path(r'^participante/(?P<alias_participante>[a-zA-Z0-9_-]+)/$'`
Muestra el **detalle de un Participante** específico. 
Incluye información del participante.

Parámetros:

- `alias_participante`: Alias del Participante.  
- Una url que permite obtener información sobre un Participante en concreto, buscando por su `alias_participante`.   

---

[⬅️ Volver al README principal](../README.md)