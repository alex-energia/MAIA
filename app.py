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
    from maia_market_intelligence import buscar_oportunidades, detectar_activos_tempranos
except:
    def buscar_oportunidades():
        return []

    def detectar_activos_tempranos():
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
# INICIALIZAR BASE DE DATOS
# =========================
init_db()

# =========================
# REGISTRAR BLUEPRINT
# =========================
app.register_blueprint(proyectos_bp)

# =========================
# PAGINA PRINCIPAL
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# PAGINA PROYECTOS
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

    nombre = data.get("nombre")
    tecnologia = data.get("tecnologia")
    pais = data.get("pais")
    ciudad = data.get("ciudad")
    moneda = data.get("moneda")
    horizonte = data.get("horizonte")
    potencia = data.get("potencia")
    unidad = data.get("unidad")

    conn = get_db()

    conn.execute(
        """
        INSERT INTO proyectos_guardados
        (titulo, tecnologia, pais, ciudad, moneda, horizonte, potencia, unidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (nombre, tecnologia, pais, ciudad, moneda, horizonte, potencia, unidad)
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
# ENERGY HARVESTER
# =========================
def maia_energy_harvester():

    queries = [
        "hydropower project for sale",
        "small hydro investment opportunity",
        "renewable energy investment opportunity"
    ]

    resultados = []

    for q in queries:

        try:

            r = requests.get(
                "https://duckduckgo.com/html/",
                params={"q": q},
                timeout=5
            )

            if r.status_code == 200:

                bloques = r.text.split("result__a")

                for b in bloques[1:3]:

                    try:

                        titulo = b.split(">")[1].split("<")[0]
                        link = b.split('href="')[1].split('"')[0]

                        resultados.append({

                            "titulo": titulo,
                            "pais": "web",
                            "tipo_activo": "energia",
                            "capacidad_mw": "N/D",
                            "empresa": "fuente web",
                            "contacto": link

                        })

                    except:
                        pass

        except:
            pass

    return resultados

# =========================
# OPORTUNIDADES MAIA
# =========================
@app.route("/maia_oportunidades")
def maia_oportunidades():

    resultados = []

    try:
        resultados.extend(buscar_oportunidades())
    except:
        pass

    try:
        resultados.extend(maia_energy_harvester())
    except:
        pass

    return jsonify({

        "total_oportunidades": len(resultados),
        "oportunidades": resultados

    })

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

    elif "riesgo" in pregunta:
        respuesta = "El riesgo depende del CAPEX, ingresos y mercado."

    return jsonify({"reply": respuesta})

# =========================
# MODULO MAIA DRONE
# =========================
@app.route("/maia_drone")
def maia_drone():
    return render_template("maia_drone.html")

# =========================
# SIMULADOR DRONE
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
# MAIA AI DRONE ARCHITECT
# =========================
@app.route("/maia_ai_drone_architect")
def maia_ai_drone_architect():
    return render_template("maia_ai_drone_architect.html")

# =========================
# MAIA AUTONOMOUS DRONE LAB
# =========================
@app.route("/maia_autonomous_lab")
def maia_autonomous_lab():
    return render_template("maia_autonomous_lab.html")

# =========================
# GENERADOR IA DE DRONES
# =========================
@app.route("/maia_generar_drone")
def maia_generar_drone():

    nombres = [
        "Ocean Explorer",
        "Petro Scanner",
        "DeepSea Hunter",
        "Aqua Vision",
        "Hydro Scout"
    ]

    sensores = [
        "Sonar multihaz",
        "Detector de hidrocarburos",
        "Cámara submarina 4K",
        "Magnetómetro",
        "Sensor químico oceánico"
    ]

    drone = {

        "nombre": random.choice(nombres),
        "tipo": "Drone submarino industrial",
        "autonomia": str(random.randint(24,72)) + " horas",
        "sensores": random.sample(sensores,3),
        "ruta": "/dron_submarino_petroleo"

    }

    return jsonify(drone)

# =========================
# DRONES APROBADOS
# =========================
@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():

    try:

        with open("ideas_drones.json", "r") as f:
            ideas = json.load(f)

        aprobados = [i for i in ideas if i["estado"] == "aprobado"]

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
# MOTOR DE SIMULACION
# =========================
@app.route("/maia_simulation_data")
def maia_simulation_data():

    if sim_engine:

        data = sim_engine.update()
        return jsonify(data)

    return jsonify([])

# =========================
# SIMULACION BASICA
# =========================
@app.route("/maia_drone_simular", methods=["POST"])
def maia_drone_simular():

    resultado = {

        "estado": "simulacion ejecutada",
        "duracion": "30s",
        "resultado": "exitoso"

    }

    return jsonify(resultado)

# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# =========================
# EJECUTAR APP
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )