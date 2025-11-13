from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import mysql.connector
import csv
from datetime import datetime, timedelta
from functools import wraps

# ---------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------------------------------------
app = Flask(__name__)
ultima_revision_alertas = None
app.secret_key = 'clave_segura_sgmcl_2025'
app.permanent_session_lifetime = timedelta(minutes=30)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="changocome",
    database="sgmcl"
)

# ---------------------------------------------------------
# FUNCIÓN GLOBAL: CONTAR ALERTAS PARA LA SIDEBAR
# ---------------------------------------------------------
@app.context_processor
def contar_alertas():
    global ultima_revision_alertas
    cursor = db.cursor(dictionary=True)

    # Fallas recientes con tarea NO completada
    cursor.execute("""
        SELECT COUNT(DISTINCT f.id) AS total
        FROM fallas f
        JOIN tareas t ON t.id_falla = f.id
        WHERE f.fecha_reporte >= NOW() - INTERVAL 3 DAY
          AND t.estado <> 'Completada';
    """)
    fallas_recientes = cursor.fetchone()['total']

    # Tareas vencidas
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tareas
        WHERE estado <> 'Completada'
          AND fecha_limite < NOW();
    """)
    tareas_vencidas = cursor.fetchone()['total']

    # Repuestos bajos o agotados
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM repuestos
        WHERE cantidad <= stock_minimo;
    """)
    repuestos_bajos = cursor.fetchone()['total']

    cursor.close()

    total_alertas = fallas_recientes + tareas_vencidas + repuestos_bajos

    # 🔁 Si ya se revisaron alertas hace poco, se considera leído
    if ultima_revision_alertas:
        # Si la última revisión fue en los últimos 60 segundos, limpiar contador
        if (datetime.now() - ultima_revision_alertas).total_seconds() < 60:
            total_alertas = 0

    return dict(alertas_pendientes=total_alertas)

# ---------------------------------------------------------
# DECORADOR DE LOGIN Y ROLES
# ---------------------------------------------------------
def login_requerido(rol_permitido=None):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('login'))
            if rol_permitido and session.get('rol') not in rol_permitido:
                flash("No tienes permisos para acceder a esta sección.", "error")
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return wrapper
    return decorador

# ---------------------------------------------------------
# LOGIN Y LOGOUT
# ---------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s", (usuario, contrasena))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['usuario'] = user['usuario']
            session['rol'] = user['rol']
            flash(f"Bienvenido, {user['nombre']} ({user['rol']})", "success")
            return redirect(url_for('index'))
        else:
            flash("Usuario o contraseña incorrectos", "error")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('login'))

# ---------------------------------------------------------
# INVENTARIO (INICIO)
# ---------------------------------------------------------
@app.route('/')
@login_requerido(['Administrador', 'Técnico'])
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, e.nombre, t.nombre AS tipo, e.marca, e.modelo, e.estado, e.ubicacion
        FROM equipos e
        JOIN tipos_equipo t ON e.id_tipo = t.id
    """)
    equipos = cursor.fetchall()
    cursor.close()
    return render_template('inventario.html', equipos=equipos)

# ---------------------------------------------------------
# REGISTRO DE NUEVOS EQUIPOS
# ---------------------------------------------------------
@app.route('/equipos/nuevo', methods=['GET', 'POST'])
@login_requerido(['Administrador'])
def nuevo_equipo():
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        id_tipo = request.form['id_tipo']
        marca = request.form['marca']
        modelo = request.form['modelo']
        ubicacion = request.form['ubicacion']

        cursor.execute("""
            INSERT INTO equipos (nombre, id_tipo, marca, modelo, estado, ubicacion)
            VALUES (%s, %s, %s, %s, 'Operativo', %s)
        """, (nombre, id_tipo, marca, modelo, ubicacion))
        db.commit()
        cursor.close()
        flash('Equipo registrado correctamente.', 'success')
        return redirect(url_for('index'))

    cursor.execute("SELECT id, nombre FROM tipos_equipo;")
    tipos = cursor.fetchall()
    cursor.close()
    return render_template('nuevo_equipo.html', tipos=tipos)


# ---------------------------------------------------------
# REPUESTOS
# ---------------------------------------------------------
@app.route('/repuestos')
@login_requerido(['Administrador', 'Técnico'])
def ver_repuestos():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM repuestos;")
    repuestos = cursor.fetchall()
    cursor.close()

    for r in repuestos:
        if r['cantidad'] <= 0:
            r['estado_stock'] = 'danger'
            r['mensaje_stock'] = 'Se necesita restock'
        elif r['cantidad'] <= r['stock_minimo']:
            r['estado_stock'] = 'warning'
            r['mensaje_stock'] = 'Stock bajo'
        else:
            r['estado_stock'] = 'ok'
            r['mensaje_stock'] = 'Suficiente stock'

    return render_template('repuestos.html', repuestos=repuestos)

# ---------------------------------------------------------
# REGISTRO DE NUEVOS REPUESTOS
# ---------------------------------------------------------
@app.route('/repuestos/nuevo', methods=['GET', 'POST'])
@login_requerido(['Administrador'])
def nuevo_repuesto():
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        cantidad = int(request.form['cantidad'])
        stock_minimo = int(request.form['stock_minimo'])

        cursor.execute("""
            INSERT INTO repuestos (nombre, tipo, cantidad, stock_minimo)
            VALUES (%s, %s, %s, %s)
        """, (nombre, tipo, cantidad, stock_minimo))
        db.commit()
        cursor.close()
        flash('Repuesto agregado correctamente.', 'success')
        return redirect(url_for('ver_repuestos'))

    cursor.close()
    return render_template('nuevo_repuesto.html')


# ---------------------------------------------------------
# REGISTRO DE FALLAS
# ---------------------------------------------------------
@app.route('/fallas', methods=['GET', 'POST'])
@login_requerido(['Administrador', 'Técnico'])
def registrar_falla():
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        descripcion = request.form['descripcion']
        prioridad = request.form['prioridad']

        # Insertar la falla
        cursor.execute("INSERT INTO fallas (id_equipo, descripcion) VALUES (%s, %s)", (id_equipo, descripcion))
        db.commit()
        id_falla = cursor.lastrowid

        # Definir fecha límite por prioridad
        dias = 2 if prioridad == 'Alta' else (14 if prioridad == 'Media' else 60)
        fecha_limite = datetime.now() + timedelta(days=dias)

        # Crear tarea correctiva automática
        cursor.execute("""
            INSERT INTO tareas (id_falla, prioridad, fecha_limite)
            VALUES (%s, %s, %s)
        """, (id_falla, prioridad, fecha_limite))
        db.commit()

        cursor.close()
        return redirect(url_for('registrar_falla'))

    cursor.execute("SELECT id, nombre FROM equipos ORDER BY nombre;")
    equipos = cursor.fetchall()
    cursor.close()
    return render_template('fallas.html', equipos=equipos)

# ---------------------------------------------------------
# TAREAS
# ---------------------------------------------------------
@app.route('/tareas')
@login_requerido(['Administrador', 'Técnico'])
def ver_tareas():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            t.id,
            e.nombre AS equipo,
            t.prioridad,
            t.fecha_creacion,
            t.fecha_limite,
            t.estado,
            t.observaciones
        FROM tareas t
        JOIN fallas f ON t.id_falla = f.id
        JOIN equipos e ON f.id_equipo = e.id
        ORDER BY t.fecha_creacion DESC;
    """)
    tareas = cursor.fetchall()
    cursor.close()

    hoy = datetime.now()
    for t in tareas:
        if t['fecha_limite']:
            t['dias_restantes'] = (t['fecha_limite'] - hoy).days
        else:
            t['dias_restantes'] = None

        if t['estado'] == 'Completada':
            t['color'] = 'ok'
        elif t['estado'] == 'En proceso':
            t['color'] = 'warning'
        elif t['estado'] == 'Pendiente' and t['dias_restantes'] is not None and t['dias_restantes'] <= 0:
            t['color'] = 'danger'
        else:
            t['color'] = 'normal'

    return render_template('tareas.html', tareas=tareas)

@app.route('/tareas/actualizar', methods=['POST'])
@login_requerido(['Administrador', 'Técnico'])
def actualizar_tarea():
    id_tarea = request.form['id_tarea']
    nuevo_estado = request.form['estado']
    observaciones = request.form['observaciones']

    cursor = db.cursor()
    cursor.execute("""
        UPDATE tareas
        SET estado = %s, observaciones = %s
        WHERE id = %s
    """, (nuevo_estado, observaciones, id_tarea))
    db.commit()

    if nuevo_estado == 'Completada':
        cursor.execute("SELECT f.id_equipo FROM tareas t JOIN fallas f ON t.id_falla = f.id WHERE t.id = %s", (id_tarea,))
        id_equipo = cursor.fetchone()[0]
        cursor.execute("UPDATE equipos SET estado = 'Operativo' WHERE id = %s", (id_equipo,))
        db.commit()
        cursor.execute("""
            INSERT INTO historial (id_tarea, descripcion)
            VALUES (%s, %s)
        """, (id_tarea, f"Tarea completada correctamente para equipo ID {id_equipo}"))
        db.commit()

    cursor.close()
    return redirect(url_for('ver_tareas'))

# ---------------------------------------------------------
# HISTORIAL
# ---------------------------------------------------------
@app.route('/historial')
@login_requerido(['Administrador'])
def ver_historial():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            h.id,
            e.nombre AS equipo,
            t.prioridad,
            t.fecha_creacion,
            h.fecha_cierre,
            h.descripcion,
            t.observaciones
        FROM historial h
        JOIN tareas t ON h.id_tarea = t.id
        JOIN fallas f ON t.id_falla = f.id
        JOIN equipos e ON f.id_equipo = e.id
        ORDER BY h.fecha_cierre DESC;
    """)
    historial = cursor.fetchall()
    cursor.close()
    return render_template('historial.html', historial=historial)

@app.route('/exportar_historial')
def exportar_historial():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            h.id,
            e.nombre AS equipo,
            t.prioridad,
            t.fecha_creacion,
            h.fecha_cierre,
            h.descripcion,
            t.observaciones
        FROM historial h
        JOIN tareas t ON h.id_tarea = t.id
        JOIN fallas f ON t.id_falla = f.id
        JOIN equipos e ON f.id_equipo = e.id
        ORDER BY h.fecha_cierre DESC;
    """)
    historial = cursor.fetchall()
    cursor.close()

    cabecera = ['ID', 'Equipo', 'Prioridad', 'Fecha creación', 'Fecha cierre', 'Descripción', 'Observaciones']
    filas = [cabecera]
    for h in historial:
        filas.append([
            h['id'],
            h['equipo'],
            h['prioridad'],
            h['fecha_creacion'].strftime('%Y-%m-%d'),
            h['fecha_cierre'].strftime('%Y-%m-%d') if h['fecha_cierre'] else '',
            h['descripcion'] or '',
            h['observaciones'] or ''
        ])

    output = make_response("\n".join([",".join(map(str, fila)) for fila in filas]))
    output.headers["Content-Disposition"] = "attachment; filename=historial_mantenimientos.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# ---------------------------------------------------------
# ALERTAS / NOTIFICACIONES
# ---------------------------------------------------------
@app.route('/alertas')
@login_requerido(['Administrador', 'Técnico'])
def ver_alertas():
    global ultima_revision_alertas
    ultima_revision_alertas = datetime.now()

    cursor = db.cursor(dictionary=True)
    alertas = []

    # Fallas recientes (no completadas)
    cursor.execute("""
        SELECT DISTINCT f.id, e.nombre AS equipo, f.fecha_reporte
        FROM fallas f
        JOIN equipos e ON f.id_equipo = e.id
        JOIN tareas t ON t.id_falla = f.id
        WHERE f.fecha_reporte >= NOW() - INTERVAL 3 DAY
          AND t.estado <> 'Completada'
        ORDER BY f.fecha_reporte DESC;
    """)
    fallas_recientes = cursor.fetchall()
    for f in fallas_recientes:
        alertas.append({
            'tipo': 'Falla nueva',
            'mensaje': f"Nueva falla en el equipo {f['equipo']}",
            'fecha': f['fecha_reporte'].strftime("%d/%m/%Y %H:%M")
        })

    # Tareas vencidas
    cursor.execute("""
        SELECT t.id, e.nombre AS equipo, t.fecha_limite
        FROM tareas t
        JOIN fallas f ON t.id_falla = f.id
        JOIN equipos e ON f.id_equipo = e.id
        WHERE t.estado <> 'Completada' AND t.fecha_limite < NOW()
        ORDER BY t.fecha_limite DESC;
    """)
    tareas_vencidas = cursor.fetchall()
    for t in tareas_vencidas:
        alertas.append({
            'tipo': 'Tarea vencida',
            'mensaje': f"La tarea del equipo {t['equipo']} está vencida.",
            'fecha': t['fecha_limite'].strftime("%d/%m/%Y %H:%M")
        })

    # 🟡 Tareas próximas a vencer (dentro de 2 días)
    cursor.execute("""
        SELECT t.id, e.nombre AS equipo, t.fecha_limite
        FROM tareas t
        JOIN fallas f ON t.id_falla = f.id
        JOIN equipos e ON f.id_equipo = e.id
        WHERE t.estado <> 'Completada'
        AND t.fecha_limite BETWEEN NOW() AND NOW() + INTERVAL 2 DAY
        ORDER BY t.fecha_limite ASC;
    """)
    tareas_proximas = cursor.fetchall()
    for t in tareas_proximas:
        alertas.append({
            'tipo': 'Tarea próxima a vencer',
            'mensaje': f"La tarea del equipo {t['equipo']} vence pronto.",
            'fecha': t['fecha_limite'].strftime("%d/%m/%Y %H:%M")
        })

    # Repuestos críticos o agotados
    cursor.execute("""
        SELECT nombre, cantidad, stock_minimo
        FROM repuestos
        WHERE cantidad <= stock_minimo;
    """)
    repuestos_bajos = cursor.fetchall()
    for r in repuestos_bajos:
        msg = "agotado" if r['cantidad'] == 0 else "en nivel crítico"
        alertas.append({
            'tipo': 'Stock crítico',
            'mensaje': f"El repuesto {r['nombre']} está {msg}.",
            'fecha': datetime.now().strftime("%d/%m/%Y %H:%M")
        })

    cursor.close()
    alertas = sorted(alertas, key=lambda x: x['fecha'], reverse=True)
    return render_template('alertas.html', alertas=alertas)

# ---------------------------------------------------------
# API: Contador dinámico de alertas
# ---------------------------------------------------------
@app.route('/contador_alertas')
def contador_alertas_api():
    cursor = db.cursor(dictionary=True)

    # Fallas recientes (no completadas)
    cursor.execute("""
        SELECT COUNT(DISTINCT f.id) AS total
        FROM fallas f
        LEFT JOIN tareas t ON t.id_falla = f.id
        WHERE f.fecha_reporte >= NOW() - INTERVAL 3 DAY
        AND (t.estado IS NULL OR t.estado <> 'Completada');
    """)
    fallas_recientes = cursor.fetchone()['total']

    # Tareas vencidas o próximas a vencer
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tareas
        WHERE estado <> 'Completada'
        AND (fecha_limite < NOW() OR fecha_limite BETWEEN NOW() AND NOW() + INTERVAL 2 DAY);
    """)
    tareas_alerta = cursor.fetchone()['total']

    # Repuestos bajos o agotados
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM repuestos
        WHERE cantidad <= stock_minimo;
    """)
    repuestos_bajos = cursor.fetchone()['total']

    cursor.close()

    total = fallas_recientes + tareas_alerta + repuestos_bajos
    return {"total": total}


# ---------------------------------------------------------
# EJECUCIÓN
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
