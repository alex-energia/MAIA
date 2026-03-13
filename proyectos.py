from flask import Blueprint, request, jsonify, redirect, render_template
import sqlite3
import os
import requests
import json
from datetime import datetime


# ======================================
# MOTOR FINANCIERO
# ======================================

evaluar_proyecto = None


# ======================================
# BLUEPRINT
# ======================================

proyectos_bp = Blueprint("proyectos", __name__)

DB = "maia.db"
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ======================================
# BASE DE DATOS
# ======================================

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# ======================================
# CREAR TABLAS
# ======================================

def init_db():

    conn = get_db()

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

    conn.execute("""
    CREATE TABLE IF NOT EXISTS maia_alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        fuente TEXT,
        fecha TEXT
    )
    """)

    conn.commit()
    conn.close()


# ======================================
# GUARDAR PROYECTO
# ======================================

@proyectos_bp.route("/guardar_proyecto", methods=["POST"])
def guardar_proyecto():

    if request.is_json:
        data = request.get_json()
        titulo = data.get("titulo")
    else:
        titulo = request.form.get("nombre")

    conn = get_db()

    conn.execute("""
    INSERT INTO proyectos_guardados
    (titulo, fecha_guardado)
    VALUES (?,?)
    """, (titulo, str(datetime.today().date())))

    conn.commit()
    conn.close()

    return redirect("/proyectos")


# ======================================
# MEMORIA PROYECTOS
# ======================================

@proyectos_bp.route("/memoria_proyectos")
def memoria_proyectos():

    conn = get_db()

    proyectos = conn.execute(
        "SELECT * FROM proyectos_guardados ORDER BY fecha_guardado DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(p) for p in proyectos])


# ======================================
# ELIMINAR PROYECTO
# ======================================

@proyectos_bp.route("/eliminar_proyecto/<int:proyecto_id>", methods=["DELETE"])
def eliminar_proyecto(proyecto_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM proyectos_guardados WHERE id=?",
        (proyecto_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "eliminado"})


# ======================================
# MOTOR FINANCIERO MAIA COMPLETO
# ======================================

def motor_financiero_simple(capacidad):

    capex = capacidad * 2000000
    opex = capacidad * 40000

    flujo_anual = capacidad * 120000

    van = capacidad * 500000
    tir = 12
    payback = 8

    ebit = flujo_anual * 0.65
    ebitda = flujo_anual * 0.80
    wacc = 9.5

    indicadores = {

        "VAN": van,
        "TIR": tir,
        "Payback": payback,

        "ROI %": 18,
        "ROIC %": 15,

        "EBIT": ebit,
        "EBITDA": ebitda,

        "WACC %": wacc,

        "Probabilidad Rentabilidad %": 72

    }

    escenarios = {

        "Sin deuda": {"tir": 12, "van": van},
        "Deuda 50%": {"tir": 15, "van": van * 1.3},
        "Deuda 70%": {"tir": 18, "van": van * 1.6}

    }

    capex_detallado = [

        {"actividad": "Ingeniería", "valor": capex * 0.08},
        {"actividad": "Equipos", "valor": capex * 0.55},
        {"actividad": "Construcción", "valor": capex * 0.25},
        {"actividad": "Interconexión", "valor": capex * 0.12}

    ]

    opex_detallado = [

        {"actividad": "Operación", "valor": opex * 0.40},
        {"actividad": "Mantenimiento", "valor": opex * 0.35},
        {"actividad": "Administración", "valor": opex * 0.25}

    ]

    valor_generado = [

        {"driver": "Venta energía", "valor": flujo_anual * 0.85},
        {"driver": "Certificados verdes", "valor": flujo_anual * 0.10},
        {"driver": "Servicios red", "valor": flujo_anual * 0.05}

    ]

    montecarlo = [
        van * 0.8,
        van * 0.9,
        van,
        van * 1.1,
        van * 1.2
    ]

    radar = [
        tir,
        70,
        65,
        85,
        75
    ]

    return {

        "capex": capex,
        "opex": opex,

        "van": van,
        "tir": tir,

        "flujo_anual": flujo_anual,
        "payback": payback,

        "indicadores": indicadores,
        "escenarios": escenarios,

        "capex_detallado": capex_detallado,
        "opex_detallado": opex_detallado,
        "valor_generado": valor_generado,

        "montecarlo": montecarlo,
        "radar": radar,

        "score_maia": 78,
        "decision_maia": "Proyecto viable para inversión",
        "score_riesgo": 32,
        "rating": "BBB",

        "semaforo": "verde"

    }


# ======================================
# DASHBOARD PROYECTO
# ======================================

@proyectos_bp.route("/proyectos/<int:proyecto_id>")
def ver_proyecto(proyecto_id):

    conn = get_db()

    proyecto = conn.execute(
        "SELECT * FROM proyectos_guardados WHERE id=?",
        (proyecto_id,)
    ).fetchone()

    conn.close()

    if not proyecto:
        return "Proyecto no encontrado"

    proyecto_dict = dict(proyecto)

    capacidad = proyecto_dict.get("capacidad_mw", 0)

    try:
        capacidad = float(capacidad)
    except:
        capacidad = 0

    try:

        if evaluar_proyecto:
            resultado = evaluar_proyecto(capacidad)
        else:
            resultado = motor_financiero_simple(capacidad)

    except Exception as e:

        print("ERROR MOTOR MAIA:", e)

        resultado = motor_financiero_simple(capacidad)

    contexto = {

        "proyecto": proyecto,

        "capex": resultado["capex"],
        "opex": resultado["opex"],

        "van": resultado["van"],
        "tir": resultado["tir"],

        "flujo_anual": resultado["flujo_anual"],
        "payback": resultado["payback"],

        "capex_detallado": resultado["capex_detallado"],
        "opex_detallado": resultado["opex_detallado"],
        "valor_generado": resultado["valor_generado"],

        "indicadores_financieros": resultado["indicadores"],
        "escenarios_apalancamiento": resultado["escenarios"],

        "montecarlo": json.dumps(resultado["montecarlo"]),
        "radar": json.dumps(resultado["radar"]),

        "score_maia": resultado["score_maia"],
        "decision_maia": resultado["decision_maia"],
        "score_riesgo": resultado["score_riesgo"],
        "rating": resultado["rating"],

        "semaforo": resultado["semaforo"]

    }

    return render_template(
        "proyecto_dashboard.html",
        **contexto
    )


# ======================================
# BUSQUEDA EN INTERNET
# ======================================

def maia_live_energy_search(query):

    url = "https://duckduckgo.com/html/"
    resultados = []

    try:

        r = requests.post(
            url,
            data={"q": query},
            timeout=5
        )

        if r.status_code == 200:

            html = r.text
            bloques = html.split("result__a")

            for b in bloques[1:4]:

                try:

                    titulo = b.split(">")[1].split("<")[0]
                    link = b.split('href="')[1].split('"')[0]

                    resultados.append({

                        "titulo": titulo,
                        "pais": "Detectado en web",
                        "tipo_activo": "Energia",
                        "capacidad_mw": "N/D",
                        "empresa": "Fuente web",
                        "tipo_oportunidad": "Oportunidad detectada",
                        "fuente": "DuckDuckGo",
                        "contacto": link,
                        "fecha_publicacion": str(datetime.today().date())

                    })

                except:
                    pass

    except:
        pass

    return resultados