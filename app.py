from flask import Flask, render_template, request, jsonify, redirect
from proyectos import proyectos_bp, init_db, get_db

import requests
import os
import json
import random


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
# MAIA DRONE
# =========================
@app.route("/maia_drone")
def maia_drone():
    return render_template("maia_drone.html")


# =========================
# MAIA SIMULADOR
# =========================
@app.route("/maia_simulador")
def maia_simulador():
    return render_template("maia_simulador.html")


# =========================
# DRONE SUBMARINO PETROLEO
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
# MAIA GEO SCANNER
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
# MAIA AI DRONE ARCHITECT
# =========================
@app.route("/maia_ai_drone_architect")
def maia_ai_drone_architect():
    return render_template("maia_ai_drone_architect.html")


# =========================
# MAIA AUTONOMOUS LAB
# =========================
@app.route("/maia_autonomous_lab")
def maia_autonomous_lab():
    return render_template("maia_autonomous_lab.html")


# =========================
# GENERAR DRONE IA
# =========================
@app.route("/maia_generar_drone")
def maia_generar_drone():

    ideas = [

        {
            "nombre": "Drone médico de emergencia",
            "impacto": "Entrega desfibriladores en ciudades",
            "tipo": "Salud",
            "ruta": "/maia_autonomous_lab"
        },

        {
            "nombre": "Drone limpiador de océanos",
            "impacto": "Recolecta plástico del mar",
            "tipo": "Medio ambiente",
            "ruta": "/maia_autonomous_lab"
        },

        {
            "nombre": "Drone forestal anti incendios",
            "impacto": "Detecta incendios antes de propagarse",
            "tipo": "Protección ambiental",
            "ruta": "/maia_autonomous_lab"
        },

        {
            "nombre": "Drone explorador geotérmico",
            "impacto": "Detecta energía geotérmica",
            "tipo": "Energía",
            "ruta": "/maia_autonomous_lab"
        },

        {
            "nombre": "Drone detector fugas de gas",
            "impacto": "Previene explosiones en ciudades",
            "tipo": "Seguridad urbana",
            "ruta": "/maia_autonomous_lab"
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

        with open("ideas_drones.json", "r") as f:
            ideas = json.load(f)

        aprobados = [
            i for i in ideas
            if i["estado"] == "aprobado"
        ]

        return jsonify(aprobados)

    except:
        return jsonify([])


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

    try:

        with open("ideas_drones.json", "r") as f:
            ideas = json.load(f)

    except:
        ideas = []

    ideas.append(nueva)

    with open("ideas_drones.json", "w") as f:
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