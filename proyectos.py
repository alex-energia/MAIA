from flask import Blueprint, render_template, request, redirect, jsonify
import numpy as np
import numpy_financial as npf
import sqlite3
import os
import datetime
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
# CREAR TABLAS
# =========================

def init_db():

    conn = get_db()

    # TABLA PROYECTOS FINANCIEROS
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

    # =========================
    # MEMORIA PROYECTOS MAIA
    # =========================

    conn.execute("""
    CREATE TABLE IF NOT EXISTS proyectos_guardados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        pais TEXT,
        tipo_activo TEXT,
        capacidad_mw TEXT,
        fase TEXT,
        empresa TEXT,
        tipo_oportunidad TEXT,
        fuente TEXT,
        contacto TEXT,
        fecha_publicacion TEXT,
        fecha_guardado TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# GUARDAR PROYECTO MAIA
# =========================

@proyectos_bp.route("/guardar_proyecto", methods=["POST"])
def guardar_proyecto():

    data = request.get_json()

    conn = get_db()

    conn.execute("""
        INSERT INTO proyectos_guardados
        (titulo,pais,tipo_activo,capacidad_mw,fase,empresa,
        tipo_oportunidad,fuente,contacto,fecha_publicacion,fecha_guardado)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """,(
        data.get("titulo"),
        data.get("pais"),
        data.get("tipo_activo"),
        data.get("capacidad_mw"),
        data.get("fase"),
        data.get("empresa"),
        data.get("tipo_oportunidad"),
        data.get("fuente"),
        data.get("contacto"),
        data.get("fecha_publicacion"),
        str(datetime.date.today())
    ))

    conn.commit()
    conn.close()

    return jsonify({"status":"proyecto_guardado"})


# =========================
# VER MEMORIA DE PROYECTOS
# =========================

@proyectos_bp.route("/memoria_proyectos")
def memoria_proyectos():

    conn = get_db()

    proyectos = conn.execute(
        "SELECT * FROM proyectos_guardados ORDER BY fecha_guardado DESC"
    ).fetchall()

    conn.close()

    data = []

    for p in proyectos:

        data.append({
            "id":p["id"],
            "titulo":p["titulo"],
            "pais":p["pais"],
            "tipo_activo":p["tipo_activo"],
            "capacidad_mw":p["capacidad_mw"],
            "fase":p["fase"],
            "empresa":p["empresa"],
            "tipo_oportunidad":p["tipo_oportunidad"],
            "fuente":p["fuente"],
            "contacto":p["contacto"],
            "fecha_publicacion":p["fecha_publicacion"],
            "fecha_guardado":p["fecha_guardado"]
        })

    return jsonify(data)


# =========================
# ELIMINAR PROYECTO
# =========================

@proyectos_bp.route("/eliminar_proyecto/<int:proyecto_id>", methods=["DELETE"])
def eliminar_proyecto(proyecto_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM proyectos_guardados WHERE id=?",
        (proyecto_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"eliminado"})


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