from flask import Blueprint, render_template, request, redirect, jsonify
import sqlite3
import os
import pdfplumber
import pandas as pd
from docx import Document

# =========================
# BLUEPRINT
# =========================
proyectos_bp = Blueprint("proyectos", __name__)

DB = "maia.db"
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# CONEXION BASE DE DATOS
# =========================
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# CREAR TABLA
# =========================
def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        capex_inicial REAL,
        opex_anual REAL,
        ingresos_anuales REAL,
        vida_util INTEGER,
        tasa_descuento REAL
    )
    """)
    conn.commit()
    conn.close()

# =========================
# DESGLOSE CAPEX
# =========================
def desglose_capex(capex):
    return [
        {"actividad":"Ingeniería","valor":round(capex*0.15,2)},
        {"actividad":"Equipos","valor":round(capex*0.40,2)},
        {"actividad":"Construcción","valor":round(capex*0.25,2)},
        {"actividad":"Permisos","valor":round(capex*0.10,2)},
        {"actividad":"Contingencia","valor":round(capex*0.10,2)}
    ]

# =========================
# DESGLOSE OPEX
# =========================
def desglose_opex(opex):
    return [
        {"actividad":"Operación","valor":round(opex*0.35,2)},
        {"actividad":"Mantenimiento","valor":round(opex*0.25,2)},
        {"actividad":"Administración","valor":round(opex*0.15,2)},
        {"actividad":"Logística","valor":round(opex*0.15,2)},
        {"actividad":"Regulación","valor":round(opex*0.10,2)}
    ]

# =========================
# MOTOR GENERACION VALOR
# =========================
def generar_valor(capex, ingresos, opex, vida, tasa):

    flujo_operativo = ingresos - opex

    valor_ingresos = ingresos * vida
    valor_costos = opex * vida

    eficiencia_capital = flujo_operativo / capex if capex != 0 else 0

    van = 0
    for i in range(1, vida+1):
        van += flujo_operativo / ((1+tasa)**i)

    van -= capex

    valor = [
        {"driver":"Ingresos operacionales totales","valor":round(valor_ingresos,2)},
        {"driver":"Costos operacionales totales","valor":round(valor_costos,2)},
        {"driver":"Flujo operativo anual","valor":round(flujo_operativo,2)},
        {"driver":"Eficiencia del capital","valor":round(eficiencia_capital,3)},
        {"driver":"Valor presente del proyecto","valor":round(van,2)}
    ]

    return valor

# =========================
# INDICADORES FINANCIEROS
# =========================
def calcular_indicadores(capex, ingresos, opex, van):

    indicadores = {}

    if ingresos > 0:
        indicadores["Margen Operativo"] = round((ingresos - opex) / ingresos,3)

    if capex > 0:
        indicadores["Rentabilidad del Proyecto"] = round(van / capex,3)

    indicadores["EBIT"] = ingresos - opex
    indicadores["EBITDA"] = ingresos - opex

    return indicadores


# =========================
# LISTA PROYECTOS
# =========================
@proyectos_bp.route("/proyectos")
def lista_proyectos():

    conn = get_db()

    proyectos = conn.execute(
        "SELECT * FROM proyectos"
    ).fetchall()

    conn.close()

    return render_template(
        "proyectos.html",
        proyectos=proyectos
    )


# =========================
# LIMPIAR PROYECTOS
# =========================
@proyectos_bp.route("/proyectos/limpiar")
def limpiar_proyectos():

    conn = get_db()

    conn.execute("DELETE FROM proyectos")

    conn.commit()
    conn.close()

    return redirect("/proyectos")


# =========================
# CREAR PROYECTO
# =========================
@proyectos_bp.route("/proyectos/nuevo", methods=["GET","POST"])
def nuevo_proyecto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        sector = request.form["sector"]
        horizonte = int(request.form["horizonte"])
        capacidad = float(request.form["capacidad"])

        # =========================
        # MAIA CALCULA AUTOMATICO
        # =========================

        if sector == "Solar":
            capex = capacidad * 900000
            opex = capex * 0.02
            ingresos = capacidad * 160000

        elif sector == "Hidro":
            capex = capacidad * 2500000
            opex = capex * 0.03
            ingresos = capacidad * 220000

        elif sector == "Eolico":
            capex = capacidad * 1400000
            opex = capex * 0.025
            ingresos = capacidad * 180000

        elif sector == "Agro":
            capex = capacidad * 15000
            opex = capex * 0.20
            ingresos = capacidad * 8000

        else:
            capex = capacidad * 500000
            opex = capex * 0.05
            ingresos = capacidad * 100000

        vida = horizonte
        tasa = 0.10

        conn = get_db()

        conn.execute("""
        INSERT INTO proyectos
        (nombre,capex_inicial,opex_anual,ingresos_anuales,vida_util,tasa_descuento)
        VALUES (?,?,?,?,?,?)
        """,(nombre,capex,opex,ingresos,vida,tasa))

        conn.commit()
        conn.close()

        return redirect("/proyectos")

    return render_template("proyectos_form.html")


# =========================
# DASHBOARD PROYECTO
# =========================
@proyectos_bp.route("/proyectos/<int:proyecto_id>")
def dashboard_proyecto(proyecto_id):

    conn = get_db()

    proyecto = conn.execute(
        "SELECT * FROM proyectos WHERE id=?",
        (proyecto_id,)
    ).fetchone()

    conn.close()

    if not proyecto:
        return "Proyecto no encontrado"


    capex = proyecto["capex_inicial"]
    opex = proyecto["opex_anual"]
    ingresos = proyecto["ingresos_anuales"]
    vida = proyecto["vida_util"]
    tasa = proyecto["tasa_descuento"]

    flujo_anual = ingresos - opex

    flujos = [-capex]

    for i in range(vida):
        flujos.append(flujo_anual)

    van = 0

    for i,f in enumerate(flujos):
        van += f / ((1+tasa)**i)

    # PAYBACK
    acumulado = 0
    payback = None

    for i,f in enumerate(flujos):

        acumulado += f

        if acumulado > 0:
            payback = i
            break


    if van > 0:
        evaluacion = "Proyecto rentable"
        recomendacion = "Invertir"
    else:
        evaluacion = "Proyecto no rentable"
        recomendacion = "No invertir"


    capex_detallado = desglose_capex(capex)
    opex_detallado = desglose_opex(opex)

    valor_generado = generar_valor(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )

    indicadores_financieros = calcular_indicadores(
        capex,
        ingresos,
        opex,
        van
    )

    return render_template(
        "proyecto_dashboard.html",
        proyecto=proyecto,
        flujo_anual=round(flujo_anual,2),
        van=round(van,2),
        payback=payback,
        evaluacion=evaluacion,
        recomendacion=recomendacion,
        valor_generado=valor_generado,
        capex_detallado=capex_detallado,
        opex_detallado=opex_detallado,
        indicadores_financieros=indicadores_financieros
    )