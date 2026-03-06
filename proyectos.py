from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

from nexus_motor import modelo_financiero
from nexus_motor import analisis_financiero

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
            capacidad REAL,
            unidad TEXT,
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
            ("Energia Solar", "Colombia", 1000000, 0.05),
            ("Hidroelectrico", "Colombia", 2500000, 0.04),
            ("Eolico", "Colombia", 1500000, 0.05),
            ("Nuclear", "Colombia", 8000000, 0.03),
            ("Agricola", "Colombia", 8000, 0.10),
            ("Mineria", "Colombia", 50000, 0.08),
            ("Infraestructura", "Colombia", 2000000, 0.06),
            ("Inmobiliario", "Colombia", 1200, 0.07)
        ])

    # =========================
    # TABLA NEXUS
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
        capacidad = float(request.form.get("capacidad", 0) or 0)
        unidad = request.form.get("unidad", "")

        # =========================
        # MOTOR NEXUS
        # =========================

        modelo = modelo_financiero(sector, capacidad)

        capex = modelo["capex"]
        opex = modelo["opex"]
        ingresos = modelo["ingresos"]

        tasa_descuento = 10

        # =========================
        # ANALISIS FINANCIERO V2
        # =========================

        analisis = analisis_financiero(sector, capacidad)

        van = analisis["van"]
        tir = analisis["tir"]
        payback = analisis["payback"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proyectos
            (nombre, sector, pais, ciudad, moneda,
             horizonte, capacidad, unidad,
             capex_inicial, opex_anual, ingresos_anuales,
             tasa_descuento, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            nombre,
            sector,
            pais,
            ciudad,
            moneda,
            horizonte,
            capacidad,
            unidad,
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
# DASHBOARD FINANCIERO
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

    van = -capex

    for año in range(1, horizonte + 1):

        van += flujo_anual / ((1 + tasa) ** año)

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