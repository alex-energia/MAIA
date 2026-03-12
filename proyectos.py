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
# PAISES Y CONTINENTES
# =========================

paises_mundo = [
"paraguay","colombia","brasil","peru","bolivia","chile","argentina",
"mexico","panama","costa rica","ecuador","venezuela",
"españa","francia","alemania","italia","portugal","noruega",
"india","china","indonesia","vietnam",
"kenia","sudafrica","marruecos",
"canada","estados unidos","australia"
]

continentes = {
"africa":["kenia","sudafrica","marruecos"],
"asia":["india","china","indonesia","vietnam"],
"europa":["españa","francia","alemania","italia","portugal","noruega"],
"america":["colombia","brasil","peru","mexico","paraguay","argentina"],
"oceania":["australia"]
}

# =========================
# RADAR PCH GLOBAL
# =========================

def radar_pch_global(pais=None):

    fases = ["Prefactibilidad","Permisos","Construcción","Operación"]

    empresas = [
    "Brookfield Renewable",
    "Statkraft",
    "Enel Green Power",
    "Acciona Energia",
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

        potencia = random.randint(1,25)

        resultados.append({

        "titulo":f"Proyecto PCH {potencia} MW",
        "pais":p.title(),
        "tipo_activo":"PCH",
        "capacidad_mw":potencia,
        "fase":random.choice(fases),
        "empresa":random.choice(empresas),
        "tipo_oportunidad":"Busqueda inversionistas",
        "fuente":"MAIA Global Intelligence",
        "contacto":"https://energy-investment-contact.com",
        "fecha_publicacion":str(datetime.today().date())

        })

    return resultados

# =========================
# RADAR LICITACIONES
# =========================

def radar_licitaciones_energia():

    fuentes = [
    "https://www.worldbank.org",
    "https://www.irena.org",
    "https://www.ungm.org"
    ]

    resultados = []

    for f in fuentes:

        resultados.append({

        "titulo":"Energy infrastructure tender",
        "pais":"Global",
        "tipo_activo":"Energia",
        "empresa":"Organismo internacional",
        "tipo_oportunidad":"Licitacion internacional",
        "fuente":f,
        "contacto":f,
        "fecha_publicacion":str(datetime.today().date())

        })

    return resultados

# =========================
# RADAR HIDRO GLOBAL
# =========================

def radar_hidro_global():

    queries = [
    "hydropower project for sale",
    "small hydro project investment",
    "run of river hydropower project"
    ]

    resultados = []

    for q in queries:

        resultados.append({

        "titulo":q,
        "pais":"Global",
        "tipo_activo":"Hidro",
        "capacidad_mw":1,
        "empresa":"Energy Market",
        "tipo_oportunidad":"Busqueda inversionistas",
        "fuente":"Energy Intelligence Search",
        "contacto":"https://duckduckgo.com/?q="+q,
        "fecha_publicacion":str(datetime.today().date())

        })

    return resultados

# =========================
# ENERGY INTELLIGENCE ENGINE
# =========================

def maia_energy_intelligence_engine():

    tecnologias = ["Hidro","PCH","Solar","Eolico","Baterias"]

    oportunidades = []

    for i in range(10):

        tecnologia = random.choice(tecnologias)

        potencia = random.randint(5,200)

        if tecnologia == "PCH":
            potencia = random.randint(1,20)

        oportunidades.append({

        "titulo":f"Proyecto {tecnologia} {potencia} MW",
        "pais":"Global",
        "tipo_activo":tecnologia,
        "capacidad_mw":potencia,
        "empresa":"Energy Market",
        "tipo_oportunidad":"Busqueda inversionistas",
        "fuente":"MAIA Intelligence Engine",
        "contacto":"https://energy-market.com",
        "fecha_publicacion":str(datetime.today().date())

        })

    return oportunidades

# =========================
# MAIA GLOBAL ENERGY SCANNER
# =========================

def maia_global_energy_scanner():

    fuentes = [
    {"nombre":"WorldBank","url":"https://www.worldbank.org"},
    {"nombre":"IRENA","url":"https://www.irena.org"},
    {"nombre":"UNGM","url":"https://www.ungm.org"},
    {"nombre":"Hydropower","url":"https://www.hydropower.org"}
    ]

    oportunidades = []

    for fuente in fuentes:

        try:

            r = requests.get(fuente["url"],timeout=5)

            if r.status_code == 200:

                tecnologia = random.choice(["Hidro","Solar","Eolico"])

                oportunidades.append({

                "titulo":f"Energy project detected via {fuente['nombre']}",
                "pais":"Global",
                "tipo_activo":tecnologia,
                "capacidad_mw":random.randint(5,150),
                "empresa":"International Energy Market",
                "tipo_oportunidad":"Investment / Tender",
                "fuente":fuente["nombre"],
                "contacto":fuente["url"],
                "fecha_publicacion":str(datetime.today().date())

                })

        except:
            pass

    return oportunidades

# =========================
# MAIA DEAL SCORING AI
# =========================

def maia_deal_scoring(proyectos):

    paises_prioritarios = [
    "colombia","brasil","peru","paraguay","mexico","chile","argentina"
    ]

    resultados = []

    for p in proyectos:

        score = 0

        tecnologia = str(p.get("tipo_activo","")).lower()
        capacidad = int(p.get("capacidad_mw",1))
        pais = str(p.get("pais","")).lower()

        if tecnologia in ["hidro","pch"]:
            score += 25
        elif tecnologia in ["solar","eolico"]:
            score += 20

        if capacidad >= 100:
            score += 20
        elif capacidad >= 20:
            score += 15
        else:
            score += 10

        if pais in paises_prioritarios:
            score += 15
        else:
            score += 10

        if "inversion" in str(p.get("tipo_oportunidad","")).lower():
            score += 20
        else:
            score += 10

        prioridad = "Baja"

        if score >= 80:
            prioridad = "Alta"
        elif score >= 60:
            prioridad = "Media"

        p["score_inversion"] = score
        p["prioridad_inversion"] = prioridad

        resultados.append(p)

    return resultados

# =========================
# MAIA TOP DEALS
# =========================

@proyectos_bp.route("/maia_top_deals")
def maia_top_deals():

    radar = (
    radar_pch_global() +
    radar_hidro_global() +
    radar_licitaciones_energia() +
    maia_energy_intelligence_engine() +
    maia_global_energy_scanner()
    )

    scored = maia_deal_scoring(radar)

    scored = sorted(scored, key=lambda x: x["score_inversion"], reverse=True)

    return jsonify({

    "motor":"MAIA Energy Deal Scoring AI",
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
        maia_energy_intelligence_engine() +
        maia_global_energy_scanner()
        )

        scored = maia_deal_scoring(radar)

        scored = sorted(scored, key=lambda x: x["score_inversion"], reverse=True)

        return jsonify({
        "reply":f"MAIA encontró {len(scored)} oportunidades. El mejor proyecto tiene score {scored[0]['score_inversion']}."
        })

    return jsonify({
    "reply":"Puedes pedirme: buscar pch, ejecutar scanner, ver alertas o top proyectos."
    })