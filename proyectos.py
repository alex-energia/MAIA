from flask import Blueprint, request, jsonify, redirect, render_template
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
    (titulo,fecha_guardado)
    VALUES (?,?)
    """,
    (
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

    # VARIABLES QUE ESPERA EL DASHBOARD
    contexto = {
        "proyecto": proyecto,
        "semaforo": "amarillo",
        "capex": 0,
        "opex": 0,
        "van": 0,
        "tir": 0
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


# =========================
# MAIA GLOBAL HYDRO DEAL HUNTER
# =========================
def maia_hydro_deal_hunter():

    queries = [
        "hydropower project for sale",
        "small hydro power plant for sale",
        "run of river hydro investment",
        "hydropower investors wanted",
        "hydropower concession project",
        "small hydro project investment opportunity"
    ]

    resultados = []

    for q in queries:

        r = maia_live_energy_search(q)

        for item in r:
            item["tipo_activo"] = "Hidro / PCH"
            resultados.append(item)

    return resultados


# =========================
# REGISTRAR ALERTAS
# =========================
def registrar_alertas(oportunidades):

    conn = get_db()

    for o in oportunidades:

        existe = conn.execute(
            "SELECT id FROM maia_alertas WHERE titulo=?",
            (o["titulo"],)
        ).fetchone()

        if not existe:

            conn.execute(
                "INSERT INTO maia_alertas (titulo,fuente,fecha) VALUES (?,?,?)",
                (
                    o["titulo"],
                    o["fuente"],
                    str(datetime.today().date())
                )
            )

    conn.commit()
    conn.close()


# =========================
# ALERTAS
# =========================
@proyectos_bp.route("/maia_alertas")
def maia_alertas():

    conn = get_db()

    alertas = conn.execute(
        "SELECT * FROM maia_alertas ORDER BY id DESC LIMIT 10"
    ).fetchall()

    conn.close()

    return jsonify([dict(a) for a in alertas])


# =========================
# BOTON BUSCAR OPORTUNIDADES
# =========================
@proyectos_bp.route("/maia_buscar_oportunidades")
def maia_buscar_oportunidades():

    oportunidades = maia_hydro_deal_hunter()

    registrar_alertas(oportunidades)

    return jsonify({
        "motor": "MAIA Hydro Deal Hunter",
        "total": len(oportunidades),
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

    registrar_alertas(oportunidades)

    return jsonify({
        "motor": "MAIA Early Energy Asset Detector",
        "total": len(oportunidades),
        "resultados": oportunidades
    })


# =========================
# CHAT MAIA
# =========================
@proyectos_bp.route("/maia_chat", methods=["POST"])
def maia_chat():

    data = request.get_json()
    mensaje = data.get("message", "")

    if "buscar" in mensaje.lower():

        query = mensaje.replace("buscar", "").strip()

        resultados = maia_live_energy_search(query)

        registrar_alertas(resultados)

        return jsonify({
            "reply": f"MAIA encontró {len(resultados)} resultados para: {query}",
            "resultados": resultados
        })

    return jsonify({
        "reply": "Puedes decir por ejemplo: buscar pch colombia o buscar hydropower chile"
    })