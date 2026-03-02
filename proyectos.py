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
        nombre = request.form["nombre"]
        sector = request.form["sector"]
        pais = request.form["pais"]
        ciudad = request.form["ciudad"]
        moneda = request.form["moneda"]
        horizonte = request.form["horizonte"]
        capex = request.form["capex"]
        opex = request.form["opex"]
        ingresos = request.form["ingresos"]
        tasa_descuento = request.form["tasa_descuento"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proyectos
            (nombre, sector, pais, ciudad, moneda, horizonte,
             capex_inicial, opex_anual, ingresos_anuales,
             tasa_descuento, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre, sector, pais, ciudad, moneda, horizonte,
            capex, opex, ingresos,
            tasa_descuento, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    # =========================
    # CALCULOS FINANCIEROS
    # =========================
    horizonte = int(proyecto["horizonte"])
    capex = float(proyecto["capex_inicial"])
    opex = float(proyecto["opex_anual"])
    ingresos = float(proyecto["ingresos_anuales"])
    tasa = float(proyecto["tasa_descuento"]) / 100

    flujo_anual = ingresos - opex

    # VAN
    van = -capex
    for año in range(1, horizonte + 1):
        van += flujo_anual / ((1 + tasa) ** año)

    # Payback simple
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
        flujo_anual=flujo_anual,
        van=round(van, 2),
        payback=payback,
        genera_valor=genera_valor
    )