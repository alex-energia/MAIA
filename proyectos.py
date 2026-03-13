from flask import Blueprint, request, jsonify, redirect, render_template
import sqlite3
import os
import requests
from datetime import datetime

# =========================
# CONECTAR MOTOR FINANCIERO
# =========================
try:
    from nexus_motor import evaluar_proyecto
except:
    evaluar_proyecto = None


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


# =========================
# GUARDAR PROYECTO
# =========================
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
    """, (
        titulo,
        str(datetime.today().date())
    ))

    conn.commit()
    conn.close()

    return redirect("/proyectos")


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

    return jsonify({"status": "eliminado"})


# =========================
# MOTOR FINANCIERO INTERNO
# =========================
def motor_financiero_simple(capacidad):

    capex = capacidad * 2000000
    opex = capacidad * 40000
    van = capacidad * 500000
    tir = 0.12

    return {
        "capex": capex,
        "opex": opex,
        "van": van,
        "tir": tir,
        "indicadores": {
            "VAN": van,
            "TIR": tir,
            "Payback": 8,
            "ROI": 0.18
        },
        "escenarios": {
            "Sin deuda": {"tir": 0.12, "van": van},
            "Deuda 50%": {"tir": 0.15, "van": van * 1.3},
            "Deuda 70%": {"tir": 0.18, "van": van * 1.6}
        },
        "semaforo": "verde" if tir > 0.1 else "amarillo"
    }


# =========================
# VER PROYECTO (DASHBOARD)
# =========================
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

        resultado = evaluar_proyecto(capacidad)
        except:
            resultado = motor_financiero_simple(capacidad)

    except Exception as e:

        print("ERROR MOTOR MAIA:", e)
        resultado = motor_financiero_simple(capacidad)

    contexto = {
        "proyecto": proyecto,
        "semaforo": resultado.get("semaforo"),
        "capex": resultado.get("capex"),
        "opex": resultado.get("opex"),
        "van": resultado.get("van"),
        "tir": resultado.get("tir"),
        "indicadores_financieros": resultado.get("indicadores"),
        "escenarios_apalancamiento": resultado.get("escenarios")
    }

    return render_template(
        "proyecto_dashboard.html",
        **contexto
    )


# =========================
# BUSQUEDA REAL EN INTERNET
# =========================
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