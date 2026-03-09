from flask import Blueprint, render_template, request, redirect, jsonify
import numpy as np
import numpy_financial as npf
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

def calcular_indicadores(capex, ingresos, opex, vida, tasa):

    flujo = ingresos - opex
    flujos = [-capex] + [flujo]*vida

    van = 0
    for i,f in enumerate(flujos):
        van += f / ((1+tasa)**i)

    try:
        tir = npf.irr(flujos)
    except:
        tir = None

    ebit = ingresos - opex
    depreciacion = capex / vida
    ebitda = ebit + depreciacion

    margen_operativo = ebit / ingresos if ingresos else 0
    margen_ebitda = ebitda / ingresos if ingresos else 0

    roi = (flujo*vida - capex) / capex if capex else 0
    roic = ebit / capex if capex else 0

    costo_deuda = 0.10
    costo_capital = 0.15
    tasa_impuesto = 0.30

    deuda = 0.4
    capital = 0.6

    wacc = (deuda*costo_deuda*(1-tasa_impuesto)) + (capital*costo_capital)

    servicio_deuda = capex*0.4/vida if vida else 0
    dscr = flujo/servicio_deuda if servicio_deuda else None

    simulaciones = 1000
    resultados_van = []

    for i in range(simulaciones):

        ingreso_sim = ingresos*np.random.normal(1,0.1)
        opex_sim = opex*np.random.normal(1,0.1)

        flujo_sim = ingreso_sim - opex_sim

        flujos_sim = [-capex] + [flujo_sim]*vida

        van_sim = 0
        for j,f in enumerate(flujos_sim):
            van_sim += f/((1+tasa)**j)

        resultados_van.append(van_sim)

    probabilidad = sum(v>0 for v in resultados_van)/simulaciones

    indicadores = {

        "VAN": round(van,2),
        "TIR %": round(tir*100,2) if tir else None,
        "ROI %": round(roi*100,2),
        "ROIC %": round(roic*100,2),
        "EBIT": round(ebit,2),
        "EBITDA": round(ebitda,2),
        "Margen Operativo %": round(margen_operativo*100,2),
        "Margen EBITDA %": round(margen_ebitda*100,2),
        "WACC %": round(wacc*100,2),
        "DSCR": round(dscr,2) if dscr else None,
        "Probabilidad Rentabilidad %": round(probabilidad*100,2)

    }

    return indicadores


# =========================
# ESCENARIOS APALANCAMIENTO
# =========================

def escenarios_apalancamiento(capex):

    costo_deuda = 0.10
    costo_capital = 0.15
    impuesto = 0.30

    escenarios = {

        "0% deuda":{
            "deuda":0,
            "capital":capex,
            "wacc":costo_capital
        },

        "40% deuda":{
            "deuda":capex*0.4,
            "capital":capex*0.6,
            "wacc":(0.4*costo_deuda*(1-impuesto))+(0.6*costo_capital)
        },

        "70% deuda":{
            "deuda":capex*0.7,
            "capital":capex*0.3,
            "wacc":(0.7*costo_deuda*(1-impuesto))+(0.3*costo_capital)
        }

    }

    return escenarios


# =========================
# LISTA PROYECTOS
# =========================

@proyectos_bp.route("/proyectos")
def lista_proyectos():

    conn = get_db()
    proyectos = conn.execute("SELECT * FROM proyectos").fetchall()
    conn.close()

    return render_template(
        "proyectos.html",
        proyectos=proyectos
    )


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

        if sector == "Solar":
            capex = capacidad*900000
            opex = capex*0.02
            ingresos = capacidad*160000

        elif sector == "Hidro":
            capex = capacidad*2500000
            opex = capex*0.03
            ingresos = capacidad*220000

        elif sector == "Eolico":
            capex = capacidad*1400000
            opex = capex*0.025
            ingresos = capacidad*180000

        else:
            capex = capacidad*500000
            opex = capex*0.05
            ingresos = capacidad*100000

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

    flujos = [-capex] + [flujo_anual]*vida

    van = 0
    for i,f in enumerate(flujos):
        van += f/((1+tasa)**i)

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

    valor_generado = generar_valor(capex,ingresos,opex,vida,tasa)

    indicadores_financieros = calcular_indicadores(capex,ingresos,opex,vida,tasa)

    escenarios = escenarios_apalancamiento(capex)

    # =========================
    # SEMAFORO MAIA
    # =========================

    tir = indicadores_financieros.get("TIR %",0)
    dscr = indicadores_financieros.get("DSCR",0)
    prob = indicadores_financieros.get("Probabilidad Rentabilidad %",0)

    score = 0

    if tir and tir > 18:
        score += 25
    elif tir and tir > 12:
        score += 15

    if van > 0:
        score += 20

    if dscr and dscr > 1.5:
        score += 20
    elif dscr and dscr > 1.2:
        score += 10

    if payback and payback < vida/2:
        score += 15

    if prob and prob > 70:
        score += 20
    elif prob and prob > 55:
        score += 10

    if score >= 70:
        semaforo = "verde"
        decision = "Proyecto altamente atractivo"
        color_semaforo = "#16a34a"

    elif score >= 40:
        semaforo = "amarillo"
        decision = "Proyecto viable con riesgos"
        color_semaforo = "#eab308"

    else:
        semaforo = "rojo"
        decision = "Proyecto no recomendable"
        color_semaforo = "#dc2626"

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
        indicadores_financieros=indicadores_financieros,
        escenarios_apalancamiento=escenarios,

        score_maia=score,
        semaforo=semaforo,
        decision_maia=decision,
        color_semaforo=color_semaforo

    )