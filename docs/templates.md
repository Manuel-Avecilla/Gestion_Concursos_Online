# Templates del Sistema

A continuación se detallan uno por uno los requisitos solicitados en la tarea y dónde se han implementado.

---

## 5 templates tags o mas

### 1. `{% load static %}`
Este tag permite cargar los archivos estáticos del proyecto (CSS, JS, imágenes, etc.).
- [Ver tag](../app/Concursos_Online/templates/base/base.html#L1)

### 2. `{% if %}`
Sirve para ejecutar contenido condicional dentro de la plantilla.
Permite mostrar contenido solo cuando una condición es verdadera.
- [Ver tag](../app/Concursos_Online/templates/concursos/_item_concurso.html#L8)

### 3. `{% for %}`
Se usa para iterar sobre listas, QuerySets o cualquier colección.
- [Ver tag](../app/Concursos_Online/templates/concursos/_item_concurso.html#L42)

### 4. `{% empty %}`
Forma parte de un bucle for.
Se ejecuta cuando la lista está vacía.
- [Ver tag](../app/Concursos_Online/templates/concursos/_item_concurso.html#L49)

### 5. `{% url %}`
Sirve para generar enlaces de forma dinámica utilizando el nombre de la URL definida en urls.py.
- [Ver tag](../app/Concursos_Online/templates/concursos/_item_concurso.html#L44)

### 6. `{% include %}`
Sirve para incluir una plantilla dentro de otra.
Muy útil para fragmentar código repetido (como items de lista).
- [Ver tag](../app/Concursos_Online/templates/base/base.html#L29)

### 7. `{% extends %}`
Este tag permite que una plantilla herede de otra.
Es fundamental para mantener coherencia visual en todo el proyecto.
- [Ver tag](../app/Concursos_Online/templates/concursos/concurso_detalle.html#L1)

### 8. `{% block %}`
Se utiliza para definir secciones editables dentro de una plantilla base.
Las plantillas hijas pueden sobrescribir estos bloques con contenido propio.
Es esencial para implementar correctamente la herencia de plantillas en Django.
- [Ver tag](../app/Concursos_Online/templates/concursos/concurso_detalle.html#L10)

---

## 5 operadores diferentes

### 1. `>=`
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L32)

### 2. `<=`
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L36)

### 3. `==`
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L40)

### 4. `>`
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L53)

### 5. `not`
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L10)


---

## formato correcto a las fechas
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L19)

---

## 10 template filters

### 1. `cut`
Elimina una subcadena del texto.
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L5)

### 2. `truncatechars`
Limita el texto a un número de caracteres y añade “…”.
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L16)

### 3. `date`
Da formato legible a un objeto datetime.
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L19)

### 4. `length`
Devuelve el número de elementos de una lista o el tamaño de una cadena.
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L40)

### 5. `slice`
Permite cortar una lista, similar a slicing en Python.
- [Ejemplo](../app/Concursos_Online/templates/concursos/_item_concurso.html#L42)

### 6. `capfirst`
Convierte la primera letra del texto a mayúscula.
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L18)

### 7. `upper`
Convierte todo el texto a mayúsculas.
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L26)

### 8. `default`
Muestra un valor alternativo si la variable es vacía o nula.
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L27)

### 9. `add`
Realiza una suma sencilla.
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L23)

### 10.`floatformat`
Redondea un número float al formato deseado.
- [Ejemplo](../app/Concursos_Online/templates/jurados/metricas_jurados.html#L19)

---

