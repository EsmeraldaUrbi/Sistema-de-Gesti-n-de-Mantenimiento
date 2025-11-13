Sistema de Gestión de Mantenimiento Correctivo de Laboratorio (SGMCL)
Descripción:
Este proyecto es una aplicación web desarrollada en Python (Flask) y MySQL, diseñada para administrar:
- Equipos del laboratorio.
- Registro de fallas.
- Tareas correctivas.
- Inventario de repuestos.
- Alertas automáticas de mantenimiento y stock.
- Historial de mantenimientos realizados.

Requisitos previos
Antes de ejecutar el sistema, asegúrate de tener instalado:
- Python 3.10 o superior → https://www.python.org/downloads/
- MySQL Server 8.0 o superior → https://dev.mysql.com/downloads/mysql/
- MySQL Workbench (última versión) → https://dev.mysql.com/downloads/workbench/
- Visual Studio Code (opcional) → https://code.visualstudio.com/

Instalación del entorno de trabajo (Windows)
1. Abre una terminal (CMD o PowerShell) en la carpeta del proyecto.
2. Crea un entorno virtual de Python:
python -m venv venv
3. Activa el entorno virtual:
venv\Scripts\activate
4. Instala las dependencias necesarias:
pip install flask mysql-connector-python
5. instalar requeriments
pip install -r requirements.txt

Configuración de la base de datos MySQL
1. Abre MySQL Workbench y conéctate a tu servidor local.
(Por defecto el usuario es root y la contraseña puede estar vacía o ser la que tú definiste).
2. Crea la base de datos ejecutando el script sgmcl.sql incluido en el proyecto.
(Puedes pegarlo directamente en una pestaña nueva y ejecutar todo).
3. Al finalizar, deberías ver las tablas:
usuarios, tipos_equipo, equipos, fallas, tareas, repuestos, historial, alertas.
4. Comprueba que existen los usuarios iniciales ejecutando:

SELECT * FROM usuarios;

Deben aparecer:
admin / admin123 (Administrador)
juan / tecnico123 (Técnico)

Configurar conexión en app.py
En la parte superior del archivo app.py, revisa que tus credenciales de MySQL coincidan:
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="contraseña",   # cámbialo sseguramente tu MySQL tiene otra contraseña
    database="sgmcl"
)

Ejecutar el sistema
1. Activa el entorno virtual:
venv\Scripts\activate
2. Inicia el servidor Flask:
python app.py
3. Abre el navegador y entra a:
http://127.0.0.1:5000/
4. Inicia sesión con:
Administrador: usuario admin / contraseña admin123
Técnico: usuario juan / contraseña tecnico123

Estructura del proyecto
SGMCL/
│
├── app.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── inventario.html
│   ├── nuevo_equipo.html
│   ├── repuestos.html
│   ├── nuevo_repuesto.html
│   ├── fallas.html
│   ├── tareas.html
│   ├── historial.html
│   └── alertas.html
│
├── static/
│
└── sgmcl.sql

Funcionalidades principales
- Inventario: muestra todos los equipos registrados y permite agregar nuevos.
- Repuestos: gestiona piezas con alertas por stock bajo.
- Fallas: permite reportar fallas y genera automáticamente tareas correctivas.
- Tareas: lista tareas pendientes, en proceso o completadas, con fechas límite.
- Historial: registra tareas completadas.
- Alertas: notifica sobre fallas nuevas, tareas vencidas o próximas y stock crítico.
- Login / Roles: control de acceso (Administrador y Técnico).
