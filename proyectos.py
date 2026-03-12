from flask import Blueprint, request, jsonify
import sqlite3
import os
import requests
from datetime import datetime

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

    return jsonify([dict(p) for p in proyectos])

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
# BUSQUEDA REAL EN INTERNET
# =========================

def maia_live_energy_search(query):

    url = "https://duckduckgo.com/html/"

    resultados = []

    try:

        r = requests.post(url, data={"q": query}, timeout=15)

        if r.status_code == 200:

            html = r.text

            bloques = html.split("result__a")

            for b in bloques[1:8]:

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

# =========================
# BOTON BUSCAR OPORTUNIDADES
# =========================

@proyectos_bp.route("/maia_buscar_oportunidades")
def maia_buscar_oportunidades():

    queries = [

        "hydropower project for sale",
        "small hydro investors wanted",
        "renewable energy project investment opportunity",
        "energy project seeking investors",
        "run of river hydro project investment"

    ]

    oportunidades = []

    for q in queries:

        resultados = maia_live_energy_search(q)

        oportunidades.extend(resultados)

    return jsonify({

        "motor":"MAIA Global Energy Scanner",
        "resultados": oportunidades

    })

# =========================
# BOTON ACTIVOS TEMPRANOS
# =========================

@proyectos_bp.route("/maia_activos_tempranos")
def maia_activos_tempranos():

    queries = [

        "hydropower project permitting",
        "small hydro project prefeasibility",
        "hydropower concession project",
        "run of river license application",
        "hydropower environmental permit"

    ]

    oportunidades = []

    for q in queries:

        resultados = maia_live_energy_search(q)

        oportunidades.extend(resultados)

    return jsonify({

        "motor":"MAIA Early Energy Asset Detector",
        "resultados": oportunidades

    })

# =========================
# CHAT MAIA
# =========================

@proyectos_bp.route("/maia_chat", methods=["POST"])
def maia_chat():

    data = request.get_json()

    mensaje = data.get("message","")

    if "buscar" in mensaje.lower():

        query = mensaje.replace("buscar","").strip()

        resultados = maia_live_energy_search(query)

        return jsonify({

            "reply": f"MAIA encontró {len(resultados)} resultados para: {query}",
            "resultados": resultados

        })

    return jsonify({

        "reply":"Puedes escribir por ejemplo: buscar pch paraguay o buscar hydropower colombia"

    })