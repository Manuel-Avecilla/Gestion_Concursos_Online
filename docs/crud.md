## CRUD del Sistema

---

### CRUD 1 - Usuario
Representa la cuenta base de todo tipo de usuario en el sistema (participante, jurado o administrador).

**Validaciones:** ***UsuarioForm***

- Validacion nombre > 3 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L33).  
- Validacion contraseña > 8 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L36).

**Validaciones:** ***UsuarioBuscarAvanzada***

- Validacion Seleccione un tipo de Usuario [`Ver validacion`](../app/Concursos_Online/forms.py#L96).
- Validacion rango de fechas incorrecto [`Ver validacion`](../app/Concursos_Online/forms.py#L102).

**Widgets:**
- forms.DateInput [`Ver widget`](../app/Concursos_Online/forms.py#L60).

---

### CRUD 2 - Perfil
Contiene información adicional del usuario.

**Validaciones:** ***PerfilForm***

- Validacion nombre completo < 5 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L143).
- Validacion biografia < 10 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L146).
- Validacion fecha nacimiento requerida [`Ver validacion`](../app/Concursos_Online/forms.py#L149).
- Validacion fecha nacimiento futura [`Ver validacion`](../app/Concursos_Online/forms.py#L151).
- Validacion imagen tamaño > 2MB [`Ver validacion`](../app/Concursos_Online/forms.py#L157).
- Validacion formato imagen [`Ver validacion`](../app/Concursos_Online/forms.py#L162).

**Validaciones:** ***PerfilBuscarAvanzada***

- Validacion rellenar al menos un campo [`Ver validacion`](../app/Concursos_Online/forms.py#L213).
- Validacion rango de fechas incorrecto [`Ver validacion`](../app/Concursos_Online/forms.py#L227).

**Widgets:**
- forms.DateInput [`Ver widget`](../app/Concursos_Online/forms.py#L128).
- forms.ClearableFileInput [`Ver widget`](../app/Concursos_Online/forms.py#L129).
- forms.SelectMultiple [`Ver widget`](../app/Concursos_Online/forms.py#L195).


---

### CRUD 3 - Participante
Usuarios que se inscriben en concursos y suben trabajos.

**Validaciones:** ***ParticipanteForm***

- Validacion alias > 20 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L294).
- Validacion edad < 10 años [`Ver validacion`](../app/Concursos_Online/forms.py#L297).
- Validacion edad > 100 años [`Ver validacion`](../app/Concursos_Online/forms.py#L300).
- Validacion puntuacion total rango 0-100 [`Ver validacion`](../app/Concursos_Online/forms.py#L303).
- Validacion nivel rango 0-5 [`Ver validacion`](../app/Concursos_Online/forms.py#L306).

**Validaciones:** ***ParticipanteBuscarAvanzada***

- Validacion alias > 20 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L359).
- Validacion edad rango 10-100 [`Ver validacion`](../app/Concursos_Online/forms.py#L362).
- Validacion nivel rango 1-5 [`Ver validacion`](../app/Concursos_Online/forms.py#L365).

**Widgets:**
- forms.NumberInput (Edad) [`Ver widget`](../app/Concursos_Online/forms.py#L254).
- forms.NumberInput (Nivel) [`Ver widget`](../app/Concursos_Online/forms.py#L263).
- forms.NumberInput (Puntuacion) [`Ver widget`](../app/Concursos_Online/forms.py#L271).


---

### CRUD 4 - Administrador
Encargado de crear concursos y enviar notificaciones.

**Validaciones:** ***AdministradorForm***
 
- Validacion horario disponible sin estar activo [`Ver validacion`](../app/Concursos_Online/forms.py#L402).
- Validacion area responsable < 3 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L405).

**Validaciones:** ***AdministradorBuscarAvanzada***

- Validacion rellenar al menos un campo [`Ver validacion`](../app/Concursos_Online/forms.py#L472).
- Validacion area responsable > 100 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L484).
- Validacion rango horario incorrecto [`Ver validacion`](../app/Concursos_Online/forms.py#L488).
- Validacion valor activo inválido [`Ver validacion`](../app/Concursos_Online/forms.py#L491).

**Widgets:**
- forms.TimeInput [`Ver widget`](../app/Concursos_Online/forms.py#L389).
- forms.Select [`Ver widget`](../app/Concursos_Online/forms.py#L429).


---

### CRUD 5 - Jurado
Representa a los usuarios encargados de evaluar los trabajos.

**Validaciones:** ***JuradoForm***

- Validacion experiencia negativa [`Ver validacion`](../app/Concursos_Online/forms.py#L537).
- Validacion especialidad < 3 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L540).
- Validacion puntuacion media rango 0-999.99 [`Ver validacion`](../app/Concursos_Online/forms.py#L543).

**Validaciones:** ***JuradoBuscarAvanzada***

- Validacion nombre usuario > 50 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L606).
- Validacion especialidad > 100 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L609).
- Validacion experiencia minima negativa [`Ver validacion`](../app/Concursos_Online/forms.py#L612).
- Validacion puntuacion minima rango 0-100 [`Ver validacion`](../app/Concursos_Online/forms.py#L615).

**Widgets:**
- forms.SelectMultiple [`Ver widget`](../app/Concursos_Online/forms.py#L519).
- forms.NumberInput (Experiencia) [`Ver widget`](../app/Concursos_Online/forms.py#L567).
- forms.NumberInput (Puntuacion) [`Ver widget`](../app/Concursos_Online/forms.py#L584).


---

### CRUD 6 - Concurso
Representa un evento o competencia dentro del sistema.

**Validaciones:** ***ConcursoForm***

- Validacion nombre < 3 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L679).
- Validacion fecha final anterior a inicio [`Ver validacion`](../app/Concursos_Online/forms.py#L683).

**Validaciones:** ***ConcursoBuscarAvanzada***

- Validacion nombre > 100 caracteres [`Ver validacion`](../app/Concursos_Online/forms.py#L745).
- Validacion fecha final anterior a inicio [`Ver validacion`](../app/Concursos_Online/forms.py#L749).
- Validacion valor activo no reconocido [`Ver validacion`](../app/Concursos_Online/forms.py#L755).

**Widgets:**
- forms.DateTimeInput (Inicio) [`Ver widget`](../app/Concursos_Online/forms.py#L658).
- forms.DateTimeInput (Final) [`Ver widget`](../app/Concursos_Online/forms.py#L659).
- forms.SelectMultiple [`Ver widget`](../app/Concursos_Online/forms.py#L660).
- forms.Select [`Ver widget`](../app/Concursos_Online/forms.py#L731).


---


---

[⬅️ Volver al README principal](../README.md)