from flask import Flask, render_template, request, jsonify, redirect
from proyectos import proyectos_bp, init_db, get_db

import os
import json
import random
import requests


# =========================
# MOTOR DE SIMULACION MAIA
# =========================
try:
    from maia_sim.simulation_engine import sim_engine
except:
    sim_engine = None


# =========================
# IMPORTS OPCIONALES MAIA
# =========================
try:
    from maia_market_intelligence import buscar_oportunidades
except:
    def buscar_oportunidades():
        return []


try:
    from maia_global_scanner import escanear_mercado_global
except:
    def escanear_mercado_global():
        return []


# =========================
# CREAR APP
# =========================
app = Flask(__name__)


# =========================
# INICIALIZAR DB
# =========================
init_db()


# =========================
# BLUEPRINT
# =========================
app.register_blueprint(proyectos_bp)


# =========================
# RUTA BASE DEL PROYECTO
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================
# DRONES BASE
# =========================
DRONES_BASE = [

    {
        "nombre": "Drone submarino detección de petróleo",
        "ruta": "/dron_submarino_petroleo",
        "estado": "aprobado"
    },

    {
        "nombre": "MAIA Punto Eléctrico",
        "ruta": "/maia_punto_electrico",
        "estado": "aprobado"
    },

    {
        "nombre": "Drone Purificador Atmosférico",
        "ruta": "/drone_purificador_atmosferico",
        "estado": "aprobado"
    }

]


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# PROYECTOS
# =========================
@app.route("/proyectos")
def proyectos():

    conn = get_db()

    proyectos = conn.execute(
        "SELECT id, titulo as nombre FROM proyectos_guardados ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "proyectos.html",
        proyectos=proyectos
    )


# =========================
# VER PROYECTO
# =========================
@app.route("/proyectos/<int:id>")
def ver_proyecto(id):

    conn = get_db()

    proyecto = conn.execute(
        "SELECT * FROM proyectos_guardados WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if proyecto is None:
        return "Proyecto no encontrado"

    return render_template(
        "proyecto_detalle.html",
        proyecto=proyecto
    )


# =========================
# NUEVO PROYECTO
# =========================
@app.route("/proyectos/nuevo")
def nuevo_proyecto():
    return render_template("nuevo_proyecto.html")


# =========================
# GUARDAR PROYECTO
# =========================
@app.route("/guardar_proyecto", methods=["POST"])
def guardar_proyecto():

    data = request.form or request.get_json()

    conn = get_db()

    conn.execute(
        """
        INSERT INTO proyectos_guardados
        (titulo, tecnologia, pais, ciudad, moneda, horizonte, potencia, unidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("nombre"),
            data.get("tecnologia"),
            data.get("pais"),
            data.get("ciudad"),
            data.get("moneda"),
            data.get("horizonte"),
            data.get("potencia"),
            data.get("unidad"),
        ),
    )

    conn.commit()
    conn.close()

    return redirect("/proyectos")


# =========================
# ALERTAS MAIA
# =========================
@app.route("/maia_alertas")
def maia_alertas():

    conn = get_db()

    try:

        alertas = conn.execute(
            "SELECT * FROM maia_alertas ORDER BY id DESC LIMIT 10"
        ).fetchall()

    except:
        alertas = []

    conn.close()

    return jsonify([dict(a) for a in alertas])


# =========================
# CHAT MAIA
# =========================
@app.route("/maia_chat", methods=["POST"])
def maia_chat():

    data = request.get_json()

    pregunta = data.get("message", "").lower()

    respuesta = "MAIA no tiene suficiente información."

    if "van" in pregunta:
        respuesta = "El VAN mide la rentabilidad descontando flujos futuros."

    elif "tir" in pregunta:
        respuesta = "La TIR es la tasa que hace VAN = 0."

    elif "hidroelectrica" in pregunta:
        respuesta = "MAIA puede buscar ubicaciones óptimas para hidroeléctricas con drones."

    return jsonify({"reply": respuesta})


# =========================
# MAIA DRONE LAB
# =========================
@app.route("/maia_drone")
def maia_drone():
    return render_template("maia_drone.html")


# =========================
# DRONE SUBMARINO
# =========================
@app.route("/dron_submarino_petroleo")
def dron_submarino_petroleo():
    return render_template("drones/dron_submarino_petroleo.html")


# =========================
# MAIA PUNTO ELECTRICO
# =========================
@app.route("/maia_punto_electrico")
def maia_punto_electrico():
    return render_template("drones/maia_punto_electrico.html")


# =========================
# DRONE TODO TERRENO
# =========================
@app.route("/drone_todo_terreno")
def drone_todo_terreno():
    return render_template("drones/drone_todo_terreno.html")


# =========================
# DRONE DETECTOR DE MINAS
# =========================
@app.route("/drone_detector_minas")
def drone_detector_minas():
    return render_template("drones/drone_detector_minas.html")


# =========================
# DRONE PURIFICADOR ATMOSFERICO
# =========================
@app.route("/drone_purificador_atmosferico")
def drone_purificador_atmosferico():
    return render_template("drones/drone_purificador_atmosferico.html")


# =========================
# GEO SCANNER
# =========================
@app.route("/maia_geo_scan")
def maia_geo_scan():

    lat = 4 + random.random()
    lon = -75 + random.random()

    caudal = round(random.uniform(0.5, 5), 2)
    caida = round(random.uniform(10, 80), 2)

    potencia = round(
        9.81 * caudal * caida * 0.85 / 1000,
        2
    )

    return jsonify({

        "lat": lat,
        "lon": lon,
        "caudal": caudal,
        "caida": caida,
        "potencia_kw": potencia

    })


# =========================
# DRONE INVENTOR IA
# =========================
@app.route("/maia_drone_inventor")
def maia_drone_inventor():
    return render_template("maia_drone_inventor.html")


# =========================
# IA INVENTA DRONES
# =========================
@app.route("/maia_inventar_drone")
def maia_inventar_drone():

    ideas = [

        {
            "nombre": "Drone médico de emergencia",
            "impacto": "Entrega desfibriladores en ciudades",
            "energia": "batería rápida"
        },

        {
            "nombre": "Drone limpiador de océanos",
            "impacto": "Recolecta plástico del mar",
            "energia": "solar marino"
        },

        {
            "nombre": "Drone forestal anti incendios",
            "impacto": "Detecta incendios antes de propagarse",
            "energia": "batería industrial"
        },

        {
            "nombre": "Drone explorador geotérmico",
            "impacto": "Detecta energía geotérmica",
            "energia": "batería + solar"
        }

    ]

    return jsonify(random.choice(ideas))


# =========================
# GENERAR DISEÑO 3D
# =========================
@app.route("/maia_generar_diseno_3d")
def maia_generar_diseno_3d():

    modelo = {

        "estructura": "frame_drone.stl",
        "propulsores": "propellers.stl",
        "soporte_camara": "camera_mount.stl"

    }

    return jsonify(modelo)


# =========================
# DRONES APROBADOS
# =========================
@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():

    try:

        ruta = os.path.join(BASE_DIR, "ideas_drones.json")

        with open(ruta, "r") as f:
            ideas = json.load(f)

        aprobados = [
            i for i in ideas
            if i.get("estado") == "aprobado"
        ]

        if len(aprobados) == 0:
            return jsonify(DRONES_BASE)

        return jsonify(aprobados)

    except Exception as e:

        print("ERROR drones:", e)

        return jsonify(DRONES_BASE)


# =========================
# APROBAR DRONE
# =========================
@app.route("/aprobar_drone", methods=["POST"])
def aprobar_drone():

    data = request.get_json()

    nueva = {

        "nombre": data.get("nombre"),
        "ruta": data.get("ruta"),
        "estado": "aprobado"

    }

    ruta = os.path.join(BASE_DIR, "ideas_drones.json")

    try:

        with open(ruta, "r") as f:
            ideas = json.load(f)

    except:
        ideas = []

    ideas.append(nueva)

    with open(ruta, "w") as f:
        json.dump(ideas, f, indent=2)

    return jsonify({"estado": "aprobado"})


# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# =========================
# RUN
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )