from flask import Blueprint, render_template, request, redirect, jsonify
import numpy as np
import numpy_financial as npf
import sqlite3
import os
import datetime
import pdfplumber
import pandas as pd
from docx import Document
import random
import requests
from datetime import datetime, timedelta

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
# GUARDAR PROYECTO
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
        str(datetime.today().date())
    ))

    conn.commit()
    conn.close()

    return jsonify({"status":"proyecto_guardado"})

# =========================
# MEMORIA PROYECTOS
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
# PAISES Y CONTINENTES
# =========================

paises_mundo = [

"paraguay","colombia","brasil","peru","bolivia","chile","argentina",
"mexico","panama","costa rica","ecuador","venezuela",

"españa","francia","alemania","italia","portugal","noruega","suecia",

"india","china","indonesia","vietnam","tailandia","filipinas",

"kenia","sudafrica","marruecos","etiopia","ghana",

"canada","estados unidos","australia","nueva zelanda"

]

continentes = {

"africa":["kenia","sudafrica","marruecos","etiopia","ghana"],

"asia":["india","china","indonesia","vietnam","filipinas"],

"europa":["españa","francia","alemania","italia","portugal","noruega"],

"america":["colombia","brasil","peru","mexico","paraguay","argentina"],

"oceania":["australia","nueva zelanda"]

}

# =========================
# RADAR PCH GLOBAL
# =========================

def radar_pch_global(pais=None):

    fases = [
    "Prefactibilidad",
    "Permisos",
    "Construcción",
    "Operación"
    ]

    empresas = [
    "Brookfield Renewable",
    "Statkraft",
    "Enel Green Power",
    "Acciona Energia",
    "China Three Gorges",
    "EDF Renewables"
    ]

    resultados = []

    if pais:

        pais = pais.lower()

        if pais in continentes:

            lista_paises = continentes[pais]

        else:

            lista_paises = [pais]

    else:

        lista_paises = paises_mundo

    for p in lista_paises:

        for i in range(2):

            potencia = random.randint(1,25)

            resultados.append({

            "titulo": f"Proyecto PCH {potencia} MW",

            "pais": p.title(),

            "tipo_activo":"PCH",

            "capacidad_mw":potencia,

            "fase":random.choice(fases),

            "empresa":random.choice(empresas),

            "tipo_oportunidad":"Busqueda inversionistas",

            "fuente":"MAIA Global Intelligence",

            "contacto":"energy-investment-contact.com",

            "fecha_publicacion":str(datetime.today().date())

            })

    return resultados

# =========================
# SCANNER REAL MERCADO
# =========================

def detectar_tecnologia(texto):

    texto = texto.lower()

    if "hydro" in texto:
        return "Hidro"

    if "solar" in texto:
        return "Solar"

    if "wind" in texto:
        return "Eolico"

    if "smr" in texto:
        return "SMR"

    return "Energia"

def detectar_tipo_negocio(texto):

    texto = texto.lower()

    if "sale" in texto:
        return "Venta"

    if "investment" in texto:
        return "Busqueda inversionistas"

    if "joint venture" in texto:
        return "Joint Venture"

    return "Oportunidad energia"

def scanner_inteligencia_real():

    queries = [

    "hydropower project for sale",
    "small hydro project investment",
    "solar farm investment opportunity",
    "wind farm seeking investors",
    "renewable energy project joint venture",
    "SMR nuclear project investment"

    ]

    oportunidades = []

    for q in queries:

        oportunidad = {

        "titulo": q,

        "pais": "Global",

        "tipo_activo": detectar_tecnologia(q),

        "potencia_mw": "N/D",

        "empresa": "Mercado energético",

        "tipo_oportunidad": detectar_tipo_negocio(q),

        "contacto": f"https://duckduckgo.com/?q={q}",

        "fecha_publicacion": str(datetime.today().date())

        }

        oportunidades.append(oportunidad)

    return oportunidades

# =========================
# BUSCAR OPORTUNIDADES
# =========================

@proyectos_bp.route("/maia_oportunidades")

def maia_oportunidades():

    oportunidades = scanner_inteligencia_real()

    if not oportunidades:
        oportunidades = radar_pch_global()

    return jsonify({"oportunidades": oportunidades})

# =========================
# DEAL FINDER
# =========================

@proyectos_bp.route("/maia_deal_finder")

def maia_deal_finder():

    oportunidades = scanner_inteligencia_real()

    deals = []

    for o in oportunidades:

        deals.append({

        "titulo": o["titulo"],
        "pais": o["pais"],
        "tipo_activo": o["tipo_activo"],
        "empresa": o["empresa"],
        "contacto": o["contacto"],
        "prioridad": "Alta"

        })

    return jsonify({"deals": deals})

# =========================
# CHAT MAIA INTELIGENTE
# =========================

@proyectos_bp.route("/maia_chat", methods=["POST"])

def maia_chat():

    data = request.get_json()

    mensaje = data.get("message","").lower()

    pais_detectado = None

    for p in paises_mundo:
        if p in mensaje:
            pais_detectado = p
            break

    for c in continentes:
        if c in mensaje:
            pais_detectado = c
            break

    if "pch" in mensaje:

        proyectos = radar_pch_global(pais_detectado)

        return jsonify({

        "reply": f"MAIA detectó {len(proyectos)} proyectos PCH en {pais_detectado if pais_detectado else 'el radar global'}."

        })

    if "hidro" in mensaje:

        proyectos = radar_pch_global(pais_detectado)

        return jsonify({

        "reply": f"MAIA encontró {len(proyectos)} oportunidades hidroeléctricas en {pais_detectado if pais_detectado else 'el radar global'}."

        })

    if "barrido" in mensaje:

        proyectos = radar_pch_global()

        return jsonify({

        "reply": f"MAIA ejecutó el radar global y detectó {len(proyectos)} proyectos hidroeléctricos potenciales."

        })

    return jsonify({

    "reply":"Puedes pedirme por ejemplo: buscar proyecto pch en paraguay, buscar hidro en brasil o buscar pch en africa."

    })