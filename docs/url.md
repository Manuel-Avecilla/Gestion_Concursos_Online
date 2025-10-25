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


[⬅️ Volver al README principal](../README.md)