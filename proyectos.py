from flask import Blueprint, request, jsonify
import sqlite3
import os
import random
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
# PAISES
# =========================

paises_mundo = [
"paraguay","colombia","brasil","peru","bolivia","chile","argentina",
"mexico","panama","costa rica","ecuador","venezuela",
"españa","francia","alemania","italia","portugal","noruega",
"india","china","indonesia","vietnam",
"kenia","sudafrica","marruecos",
"canada","estados unidos","australia"
]

# =========================
# RADAR PCH
# =========================

def radar_pch_global():

    empresas = [
    "Brookfield Renewable",
    "Statkraft",
    "Enel Green Power",
    "Acciona Energia",
    "EDF Renewables"
    ]

    resultados = []

    for p in paises_mundo:

        potencia = random.randint(1,25)

        resultados.append({

        "titulo":f"Proyecto PCH {potencia} MW",
        "pais":p.title(),
        "tipo_activo":"PCH",
        "capacidad_mw":potencia,
        "empresa":random.choice(empresas),
        "tipo_oportunidad":"Busqueda inversionistas",
        "fuente":"MAIA Radar",
        "contacto":"https://energy-investment-contact.com",
        "fecha_publicacion":str(datetime.today().date())

        })

    return resultados

# =========================
# RADAR HIDRO
# =========================

def radar_hidro_global():

    queries = [
    "hydropower project for sale",
    "small hydro investment",
    "run of river project"
    ]

    resultados = []

    for q in queries:

        resultados.append({

        "titulo":q,
        "pais":"Global",
        "tipo_activo":"Hidro",
        "capacidad_mw":random.randint(5,80),
        "empresa":"Energy Market",
        "tipo_oportunidad":"Busqueda inversionistas",
        "fuente":"Energy Intelligence",
        "contacto":"https://duckduckgo.com/?q="+q,
        "fecha_publicacion":str(datetime.today().date())

        })

    return resultados

# =========================
# ENERGY INTELLIGENCE ENGINE
# =========================

def maia_energy_intelligence_engine():

    tecnologias = ["Hidro","PCH","Solar","Eolico"]

    oportunidades = []

    for i in range(10):

        tecnologia = random.choice(tecnologias)

        oportunidades.append({

        "titulo":f"Proyecto {tecnologia} {random.randint(5,200)} MW",
        "pais":"Global",
        "tipo_activo":tecnologia,
        "capacidad_mw":random.randint(5,200),
        "empresa":"Energy Market",
        "tipo_oportunidad":"Busqueda inversionistas",
        "fuente":"MAIA Engine",
        "contacto":"https://energy-market.com",
        "fecha_publicacion":str(datetime.today().date())

        })

    return oportunidades

# =========================
# MAIA ENERGY SCANNER
# =========================

def maia_global_energy_scanner():

    fuentes = [
    "https://www.worldbank.org",
    "https://www.irena.org",
    "https://www.ungm.org",
    "https://www.hydropower.org"
    ]

    oportunidades = []

    for f in fuentes:

        try:

            r = requests.get(f,timeout=5)

            if r.status_code == 200:

                oportunidades.append({

                "titulo":"Energy opportunity detected",
                "pais":"Global",
                "tipo_activo":random.choice(["Hidro","Solar","Eolico"]),
                "capacidad_mw":random.randint(5,150),
                "empresa":"International Energy Market",
                "tipo_oportunidad":"Investment / Tender",
                "fuente":f,
                "contacto":f,
                "fecha_publicacion":str(datetime.today().date())

                })

        except:
            pass

    return oportunidades

# =========================
# MAIA GLOBAL ENERGY HARVESTER
# =========================

def maia_global_energy_harvester():

    fuentes = [
    "https://www.worldbank.org",
    "https://www.irena.org",
    "https://www.iea.org",
    "https://www.hydropower.org"
    ]

    oportunidades = []

    for f in fuentes:

        try:

            r = requests.get(f,timeout=8)

            if r.status_code == 200:

                oportunidades.append({

                "titulo":"Harvested energy opportunity",
                "pais":"Global",
                "tipo_activo":random.choice(["Hidro","PCH","Solar","Eolico"]),
                "capacidad_mw":random.randint(5,200),
                "empresa":"Global Energy Market",
                "tipo_oportunidad":"Investment",
                "fuente":f,
                "contacto":f,
                "fecha_publicacion":str(datetime.today().date())

                })

        except:
            pass

    return oportunidades

# =========================
# DEAL SCORING AI
# =========================

def maia_deal_scoring(proyectos):

    resultados = []

    for p in proyectos:

        score = 0

        tecnologia = str(p.get("tipo_activo","")).lower()
        capacidad = int(p.get("capacidad_mw",1))

        if tecnologia in ["hidro","pch"]:
            score += 25
        else:
            score += 20

        if capacidad > 100:
            score += 25
        elif capacidad > 20:
            score += 15
        else:
            score += 10

        if "inversion" in p.get("tipo_oportunidad","").lower():
            score += 20
        else:
            score += 10

        prioridad = "Baja"

        if score >= 70:
            prioridad = "Alta"
        elif score >= 50:
            prioridad = "Media"

        p["score_inversion"] = score
        p["prioridad_inversion"] = prioridad

        resultados.append(p)

    return resultados

# =========================
# TOP DEALS
# =========================

@proyectos_bp.route("/maia_top_deals")
def maia_top_deals():

    radar = (
    radar_pch_global() +
    radar_hidro_global() +
    maia_energy_intelligence_engine() +
    maia_global_energy_scanner() +
    maia_global_energy_harvester()
    )

    scored = maia_deal_scoring(radar)

    scored = sorted(scored, key=lambda x: x["score_inversion"], reverse=True)

    return jsonify({

    "motor":"MAIA Energy Intelligence",
    "top_deals":scored[:20]

    })

# =========================
# CHAT MAIA
# =========================

@proyectos_bp.route("/maia_chat", methods=["POST"])
def maia_chat():

    data = request.get_json()
    mensaje = data.get("message","").lower()

    if "top" in mensaje:

        radar = (
        radar_pch_global() +
        radar_hidro_global() +
        maia_global_energy_harvester()
        )

        scored = maia_deal_scoring(radar)

        scored = sorted(scored, key=lambda x: x["score_inversion"], reverse=True)

        return jsonify({
        "reply":f"MAIA encontró {len(scored)} oportunidades. El mejor proyecto tiene score {scored[0]['score_inversion']}."
        })

    return jsonify({
    "reply":"Puedes pedirme: top proyectos, ejecutar scanner o buscar hidro."
    })