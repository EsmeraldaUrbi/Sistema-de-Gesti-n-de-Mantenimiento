from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import mysql.connector
from datetime import datetime, timedelta
from functools import wraps

# ---------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'clave_segura_sgmcl_2025'
app.permanent_session_lifetime = timedelta(minutes=30)

# Conexión rápida global
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="changocome",
    database="sgmcl"
)

ultima_revision_alertas = None


# ---------------------------------------------------------
# FUNCIÓN GLOBAL: CONTADOR DE ALERTAS
# ---------------------------------------------------------
@app.context_processor
def contar_alertas():
    cursor = db.cursor(dictionary=True)

    # Fallas recientes
    cursor.execute("""
        SELECT COUNT(DISTINCT f.id) AS total
        FROM fallas f
        LEFT JOIN tareas t ON t.id_falla = f.id
        WHERE f.fecha_reporte >= NOW() - INTERVAL 3 DAY
          AND (t.estado IS NULL OR t.estado <> 'Completada');
    """)
    fallas = cursor.fetchone()['total']

    # Tareas vencidas o próximas a vencer
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tareas
        WHERE estado <> 'Completada'
          AND (fecha_limite < NOW()
          OR fecha_limite BETWEEN NOW() AND NOW() + INTERVAL 2 DAY);
    """)
    tareas = cursor.fetchone()['total']

    # Stock crítico
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM repuestos
        WHERE cantidad <= stock_minimo;
    """)
    repuestos = cursor.fetchone()['total']

    cursor.close()
    return dict(alertas_pendientes=fallas + tareas + repuestos)


# ---------------------------------------------------------
# DECORADOR LOGIN + ROLES
# ---------------------------------------------------------
def login_requerido(roles=None):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('login'))
            if roles and session.get('rol') not in roles:
                flash("No tienes permisos para acceder aquí.", "error")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return wrapper
    return decorador


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND contrasena=%s",
                       (usuario, contrasena))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['usuario'] = user['usuario']
            session['rol'] = user['rol']
            flash(f"Bienvenido, {user['nombre']} ({user['rol']})", "success")
            return redirect(url_for('index'))

        flash("Credenciales incorrectas", "error")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for('login'))


# ---------------------------------------------------------
# INVENTARIO
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
# EDITAR EQUIPO ⭐ NUEVO ⭐
# ---------------------------------------------------------
@app.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido(['Administrador'])
def editar_equipo(id):

    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute("""
            UPDATE equipos
            SET nombre=%s, id_tipo=%s, marca=%s, modelo=%s, ubicacion=%s, estado=%s
            WHERE id=%s
        """, (
            request.form['nombre'],
            request.form['id_tipo'],
            request.form['marca'],
            request.form['modelo'],
            request.form['ubicacion'],
            request.form['estado'],
            id
        ))
        db.commit()
        cursor.close()

        flash("Equipo actualizado correctamente.", "success")
        return redirect(url_for('index'))

    # GET -> llenar formulario
    cursor.execute("SELECT * FROM equipos WHERE id=%s", (id,))
    equipo = cursor.fetchone()

    cursor.execute("SELECT id, nombre FROM tipos_equipo")
    tipos = cursor.fetchall()

    cursor.close()

    return render_template('editar_equipo.html', equipo=equipo, tipos=tipos)


# ---------------------------------------------------------
# ELIMINAR EQUIPO
# ---------------------------------------------------------
@app.route('/equipos/eliminar/<int:id>')
@login_requerido(['Administrador'])
def eliminar_equipo(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM equipos WHERE id=%s", (id,))
    db.commit()
    cursor.close()

    flash("Equipo eliminado", "info")
    return redirect(url_for('index'))


# ---------------------------------------------------------
# NUEVO EQUIPO
# ---------------------------------------------------------
@app.route('/equipos/nuevo', methods=['GET', 'POST'])
@login_requerido(['Administrador'])
def nuevo_equipo():
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            INSERT INTO equipos (nombre, id_tipo, marca, modelo, estado, ubicacion)
            VALUES (%s, %s, %s, %s, 'Operativo', %s)
        """, (
            request.form['nombre'],
            request.form['id_tipo'],
            request.form['marca'],
            request.form['modelo'],
            request.form['ubicacion']
        ))
        db.commit()
        cursor.close()
        flash("Equipo registrado", "success")
        return redirect(url_for('index'))

    cursor.execute("SELECT id, nombre FROM tipos_equipo")
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
    cursor.execute("SELECT * FROM repuestos")
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
# NUEVO REPUESTO
# ---------------------------------------------------------
@app.route('/repuestos/nuevo', methods=['GET', 'POST'])
@login_requerido(['Administrador'])
def nuevo_repuesto():
    if request.method == "POST":
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO repuestos (nombre, tipo, cantidad, stock_minimo)
            VALUES (%s, %s, %s, %s)
        """, (
            request.form['nombre'],
            request.form['tipo'],
            request.form['cantidad'],
            request.form['stock_minimo']
        ))
        db.commit()
        cursor.close()
        flash("Repuesto agregado", "success")
        return redirect(url_for('ver_repuestos'))

    return render_template('nuevo_repuesto.html')


# ---------------------------------------------------------
# EDITAR REPUESTO
# ---------------------------------------------------------
@app.route('/repuestos/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido(['Administrador'])
def editar_repuesto(id):
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            UPDATE repuestos
            SET nombre=%s, tipo=%s, cantidad=%s, stock_minimo=%s
            WHERE id=%s
        """, (
            request.form['nombre'],
            request.form['tipo'],
            request.form['cantidad'],
            request.form['stock_minimo'],
            id
        ))
        db.commit()
        cursor.close()

        flash("Repuesto actualizado", "success")
        return redirect(url_for('ver_repuestos'))

    cursor.execute("SELECT * FROM repuestos WHERE id=%s", (id,))
    repuesto = cursor.fetchone()
    cursor.close()

    return render_template('editar_repuesto.html', repuesto=repuesto)


# ---------------------------------------------------------
# ELIMINAR REPUESTO
# ---------------------------------------------------------
@app.route('/repuestos/eliminar/<int:id>')
@login_requerido(['Administrador'])
def eliminar_repuesto(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM repuestos WHERE id=%s", (id,))
    db.commit()
    cursor.close()

    flash("Repuesto eliminado", "info")
    return redirect(url_for('ver_repuestos'))


# ---------------------------------------------------------
# FALLAS
# ---------------------------------------------------------
@app.route('/fallas', methods=['GET', 'POST'])
@login_requerido(['Administrador', 'Técnico'])
def registrar_falla():
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        id_equipo = request.form['id_equipo']
        descripcion = request.form['descripcion']
        prioridad = request.form['prioridad']

        cursor.execute("INSERT INTO fallas (id_equipo, descripcion) VALUES (%s, %s)",
                       (id_equipo, descripcion))
        db.commit()
        id_falla = cursor.lastrowid

        dias = 2 if prioridad == 'Alta' else (14 if prioridad == 'Media' else 60)
        fecha_limite = datetime.now() + timedelta(days=dias)

        cursor.execute("""
            INSERT INTO tareas (id_falla, prioridad, fecha_limite)
            VALUES (%s, %s, %s)
        """, (id_falla, prioridad, fecha_limite))
        db.commit()

        cursor.close()
        return redirect(url_for('registrar_falla'))

    cursor.execute("SELECT id, nombre FROM equipos ORDER BY nombre")
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
        elif t['dias_restantes'] is not None and t['dias_restantes'] <= 0:
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
        SET estado=%s, observaciones=%s
        WHERE id=%s
    """, (nuevo_estado, observaciones, id_tarea))
    db.commit()

    if nuevo_estado == 'Completada':

        cursor.execute("""
            SELECT f.id_equipo
            FROM tareas t 
            JOIN fallas f ON t.id_falla = f.id
            WHERE t.id=%s
        """, (id_tarea,))
        id_equipo = cursor.fetchone()[0]

        cursor.execute("UPDATE equipos SET estado='Operativo' WHERE id=%s", (id_equipo,))
        db.commit()

        cursor.execute("""
            INSERT INTO historial (id_tarea, descripcion)
            VALUES (%s, %s)
        """, (id_tarea, f"Tarea completada para equipo ID {id_equipo}"))
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


# ---------------------------------------------------------
# EXPORTAR CSV
# ---------------------------------------------------------
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

    filas = [["ID", "Equipo", "Prioridad", "Fecha creación", "Fecha cierre", "Descripción", "Observaciones"]]

    for h in historial:
        filas.append([
            h['id'],
            h['equipo'],
            h['prioridad'],
            h['fecha_creacion'].strftime("%Y-%m-%d"),
            h['fecha_cierre'].strftime("%Y-%m-%d") if h['fecha_cierre'] else "",
            h['descripcion'] or "",
            h['observaciones'] or ""
        ])

    output = make_response("\n".join([",".join(map(str, fila)) for fila in filas]))
    output.headers["Content-Disposition"] = "attachment; filename=historial_mantenimientos.csv"
    output.headers["Content-Type"] = "text/csv"

    return output


# ---------------------------------------------------------
# ALERTAS
# ---------------------------------------------------------
@app.route('/alertas')
@login_requerido(['Administrador', 'Técnico'])
def ver_alertas():
    global ultima_revision_alertas
    ultima_revision_alertas = datetime.now()

    cursor = db.cursor(dictionary=True)
    alertas = []

    # Fallas nuevas
    cursor.execute("""
        SELECT DISTINCT f.id, e.nombre AS equipo, f.fecha_reporte
        FROM fallas f
        JOIN equipos e ON f.id_equipo = e.id
        JOIN tareas t ON t.id_falla = f.id
        WHERE f.fecha_reporte >= NOW() - INTERVAL 3 DAY
          AND t.estado <> 'Completada'
        ORDER BY f.fecha_reporte DESC;
    """)
    for f in cursor.fetchall():
        alertas.append({
            'tipo': 'Falla nueva',
            'mensaje': f"Nueva falla en {f['equipo']}",
            'fecha': f['fecha_reporte'].strftime("%d/%m/%Y %H:%M")
        })

    # Tareas vencidas
    cursor.execute("""
        SELECT t.id, e.nombre AS equipo, t.fecha_limite
        FROM tareas t
        JOIN fallas f ON t.id_falla = f.id
        JOIN equipos e ON f.id_equipo = e.id
        WHERE t.estado <> 'Completada'
          AND t.fecha_limite < NOW()
        ORDER BY t.fecha_limite DESC;
    """)
    for t in cursor.fetchall():
        alertas.append({
            'tipo': 'Tarea vencida',
            'mensaje': f"La tarea del equipo {t['equipo']} está vencida.",
            'fecha': t['fecha_limite'].strftime("%d/%m/%Y %H:%M")
        })

    # Tareas próximas a vencer
    cursor.execute("""
        SELECT t.id, e.nombre AS equipo, t.fecha_limite
        FROM tareas t
        JOIN fallas f ON t.id_falla = f.id
        JOIN equipos e ON f.id_equipo = e.id
        WHERE t.estado <> 'Completada'
          AND t.fecha_limite BETWEEN NOW() AND NOW() + INTERVAL 2 DAY
        ORDER BY t.fecha_limite ASC;
    """)
    for t in cursor.fetchall():
        alertas.append({
            'tipo': 'Tarea próxima a vencer',
            'mensaje': f"La tarea del equipo {t['equipo']} vence pronto.",
            'fecha': t['fecha_limite'].strftime("%d/%m/%Y %H:%M")
        })

    # Repuestos críticos
    cursor.execute("""
        SELECT nombre, cantidad, stock_minimo
        FROM repuestos
        WHERE cantidad <= stock_minimo;
    """)
    for r in cursor.fetchall():
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
# API: Contador dinámico
# ---------------------------------------------------------
@app.route('/contador_alertas')
def contador_alertas_api():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(DISTINCT f.id) AS total
        FROM fallas f
        LEFT JOIN tareas t ON t.id_falla = f.id
        WHERE f.fecha_reporte >= NOW() - INTERVAL 3 DAY
          AND (t.estado IS NULL OR t.estado <> 'Completada');
    """)
    fallas = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tareas
        WHERE estado <> 'Completada'
          AND (fecha_limite < NOW()
          OR fecha_limite BETWEEN NOW() AND NOW() + INTERVAL 2 DAY);
    """)
    tareas = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM repuestos
        WHERE cantidad <= stock_minimo;
    """)
    repuestos = cursor.fetchone()['total']

    cursor.close()

    return {"total": fallas + tareas + repuestos}


# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
