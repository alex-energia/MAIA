from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

proyectos_bp = Blueprint('proyectos', __name__, template_folder='templates')

DB_NAME = "maia.db"

# =========================
# CREAR BASE DE DATOS
# =========================

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # =========================
    # TABLA PROYECTOS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            sector TEXT,
            pais TEXT,
            ciudad TEXT,
            moneda TEXT,
            horizonte INTEGER,
            capex_inicial REAL,
            opex_anual REAL,
            ingresos_anuales REAL,
            tasa_descuento REAL,
            fecha_creacion TEXT
        )
    """)

    # =========================
    # TABLA COSTOS BASE
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS costos_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sector TEXT,
            pais TEXT,
            capex_base REAL,
            opex_pct REAL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM costos_base")
    total = cursor.fetchone()[0]

    if total == 0:

        cursor.executemany("""
            INSERT INTO costos_base (sector, pais, capex_base, opex_pct)
            VALUES (?, ?, ?, ?)
        """, [

            ("Energía Solar", "Colombia", 1000000, 0.05),
            ("Minería", "Colombia", 5000000, 0.08),
            ("Infraestructura", "Colombia", 3000000, 0.06),
            ("Energía Solar", "Perú", 1200000, 0.05),
            ("Minería", "Perú", 6000000, 0.09)

        ])

    # =========================
    # TABLA NEXUS (Motor Universal)
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nexus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER,
            tipo_proyecto TEXT,
            perfil_financiero TEXT,
            inversion_estructural REAL,
            ingresos_estimados REAL,
            opex_estimado REAL,
            horizonte INTEGER,
            tasa_descuento REAL,
            creado_en TEXT,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    # =========================
    # TABLA COSTOS POR CAPACIDAD
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS costos_capacidad (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_proyecto TEXT,
            costo_unitario REAL,
            unidad TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM costos_capacidad")
    total_cap = cursor.fetchone()[0]

    if total_cap == 0:

        cursor.executemany("""
            INSERT INTO costos_capacidad (tipo_proyecto, costo_unitario, unidad)
            VALUES (?, ?, ?)
        """, [

            ("Energia Solar", 1000000, "MW"),
            ("Hidroelectrico", 2500000, "MW"),
            ("Eolico", 1500000, "MW"),
            ("Nuclear", 8000000, "MW"),
            ("Agricola", 8000, "Hectareas"),
            ("Mineria", 50000, "Toneladas/año"),
            ("Infraestructura", 2000000, "Kilometros"),
            ("Inmobiliario", 1200, "m2")

        ])

    conn.commit()
    conn.close()


# =========================
# LISTAR PROYECTOS
# =========================

@proyectos_bp.route("/proyectos")
def listar_proyectos():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM proyectos ORDER BY id DESC")

    proyectos = cursor.fetchall()

    conn.close()

    return render_template("proyectos_lista.html", proyectos=proyectos)


# =========================
# CREAR PROYECTO
# =========================

@proyectos_bp.route("/proyectos/nuevo", methods=["GET", "POST"])
def nuevo_proyecto():

    if request.method == "POST":

        nombre = request.form.get("nombre", "")
        sector = request.form.get("sector", "")
        pais = request.form.get("pais", "")
        ciudad = request.form.get("ciudad", "")
        moneda = request.form.get("moneda", "")
        horizonte = int(request.form.get("horizonte", 0))
        ingresos = float(request.form.get("ingresos", 0) or 0)
        tasa_descuento = float(request.form.get("tasa_descuento", 0) or 0)

        # =========================
        # CAPACIDAD DEL PROYECTO
        # =========================

        try:
            capacidad = float(request.form.get("capacidad", 0) or 0)
        except:
            capacidad = 0

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # buscar costo base por sector y país
        cursor.execute("""
            SELECT capex_base, opex_pct
            FROM costos_base
            WHERE sector = ? AND pais = ?
        """, (sector, pais))

        costo_base = cursor.fetchone()

        if costo_base:

            capex = float(costo_base[0])
            opex = capex * float(costo_base[1])

        else:

            capex = float(request.form.get("capex", 0) or 0)
            opex = float(request.form.get("opex", 0) or 0)

        cursor.execute("""

            INSERT INTO proyectos
            (nombre, sector, pais, ciudad, moneda, horizonte,
             capex_inicial, opex_anual, ingresos_anuales,
             tasa_descuento, fecha_creacion)

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            nombre,
            sector,
            pais,
            ciudad,
            moneda,
            horizonte,
            capex,
            opex,
            ingresos,
            tasa_descuento,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ))

        conn.commit()
        conn.close()

        return redirect(url_for("proyectos.listar_proyectos"))

    return render_template("proyectos_form.html")


# ==============================
# DASHBOARD FINANCIERO PROYECTO
# ==============================

@proyectos_bp.route("/proyectos/<int:proyecto_id>/dashboard")
def dashboard_proyecto(proyecto_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM proyectos WHERE id = ?", (proyecto_id,))
    proyecto = cursor.fetchone()

    conn.close()

    if not proyecto:
        return "Proyecto no encontrado", 404

    horizonte = int(proyecto["horizonte"] or 0)
    capex = float(proyecto["capex_inicial"] or 0)
    opex = float(proyecto["opex_anual"] or 0)
    ingresos = float(proyecto["ingresos_anuales"] or 0)
    tasa = float(proyecto["tasa_descuento"] or 0) / 100

    flujo_anual = ingresos - opex

    # VAN
    van = -capex

    for año in range(1, horizonte + 1):
        van += flujo_anual / ((1 + tasa) ** año)

    # PAYBACK
    acumulado = -capex
    payback = None

    for año in range(1, horizonte + 1):

        acumulado += flujo_anual

        if acumulado >= 0 and payback is None:
            payback = año

    genera_valor = "Sí" if van > 0 else "No"

    return render_template(

        "proyecto_dashboard.html",
        proyecto=proyecto,
        flujo_anual=round(flujo_anual, 2),
        van=round(van, 2),
        payback=payback,
        genera_valor=genera_valor

    )