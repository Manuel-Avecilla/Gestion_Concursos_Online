# Instalación y ejecución en local

#### 1. Clonar el repositorio:
```bash
git clone git@github.com:Manuel-Avecilla/Gestion_Concursos_Online.git
```
#### 2. Acceder al directorio del proyecto:
```bash
cd Gestion_Concursos_Online/app/
```
#### 3. Crear un entorno virtual:
```bash
python3 -m venv myvenv
```
#### 4. Activar el entorno virtual:
```bash
source myvenv/bin/activate
```
#### 5. Actualizar `pip`:
```bash
python -m pip install --upgrade pip
```
#### 6. Instalar los requerimientos del proyecto:
```bash
pip install -r requirements.txt
```
#### 7. Crear la base de datos y aplicar migraciones:
```bash
python manage.py migrate
```
#### 8. Cargar datos iniciales:
```bash
python manage.py loaddata Concursos_Online/fixtures/datos.json
```
#### 9. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```
---

[⬅️ Volver al README principal](../README.md)