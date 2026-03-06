from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from nexus_motor import modelo_financiero, evaluar_proyecto

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
            capacidad REAL,
            unidad TEXT,
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

        nombre = request.form.get("nombre", "")
        sector = request.form.get("sector", "")
        pais = request.form.get("pais", "")
        ciudad = request.form.get("ciudad", "")
        moneda = request.form.get("moneda", "")
        horizonte = int(request.form.get("horizonte", 0))
        capacidad = float(request.form.get("capacidad", 0) or 0)
        unidad = request.form.get("unidad", "")

        modelo = modelo_financiero(sector, capacidad)

        capex = modelo["capex"]
        opex = modelo["opex"]
        ingresos = modelo["ingresos"]

        tasa_descuento = 10

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

    from nexus_motor import evaluar_proyecto

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM proyectos WHERE id = ?", (proyecto_id,))
    proyecto = cursor.fetchone()

    conn.close()

    if not proyecto:
        return "Proyecto no encontrado", 404

    sector = proyecto["sector"]
    capacidad = proyecto["capacidad"]

    analisis = evaluar_proyecto(sector, capacidad)

    capex = proyecto["capex_inicial"]
    opex = proyecto["opex_anual"]
    ingresos = proyecto["ingresos_anuales"]

    flujo_anual = ingresos - opex

    return render_template(
        "proyecto_dashboard.html",
        proyecto=proyecto,
        flujo_anual=round(flujo_anual, 2),
        van=round(analisis["van"], 2),
        tir=round(analisis["tir"], 4) if analisis["tir"] else None,
        payback=analisis["payback"],
        evaluacion=analisis["evaluacion"],
        recomendacion=analisis["recomendacion"]
    )

    # ==============================
    # INTELIGENCIA MAIA
    # ==============================

    evaluacion_maia = evaluar_proyecto(sector, capacidad)

    van = evaluacion_maia["van"]
    tir = evaluacion_maia["tir"]
    payback = evaluacion_maia["payback"]
    evaluacion = evaluacion_maia["evaluacion"]
    recomendacion = evaluacion_maia["recomendacion"]

    genera_valor = "Sí" if van > 0 else "No"

    return render_template(
        "proyecto_dashboard.html",
        proyecto=proyecto,
        flujo_anual=round(flujo_anual, 2),
        van=round(van, 2),
        tir=round(tir, 4) if tir else None,
        payback=payback,
        evaluacion=evaluacion,
        recomendacion=recomendacion,
        genera_valor=genera_valor
    )