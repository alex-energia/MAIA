from flask import Flask, render_template, request, jsonify, session
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
import math
import numpy as np
import time
import threading
import re

# 🔥 PROTECCIÓN TRIMESH
try:
    import trimesh
except:
    trimesh = None

# =========================
# APP
# =========================
app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_secret_ultra"

# =========================
# INIT
# =========================
init_db()
app.register_blueprint(proyectos_bp)

# =========================
# 🔥 LOCK GLOBAL (EMPRESA)
# =========================
lock_maia = threading.Lock()

# =========================
# 🔥 ESTADO GLOBAL
# =========================
estado_maia = {
    "progreso": 0,
    "estado": "IDLE",
    "mensaje": ""
}

resultado_global = {}

# =========================
# 🔥 LOGGER
# =========================
def log_event(tipo, mensaje):
    log = {
        "tipo": tipo,
        "mensaje": mensaje,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print("🧠 LOG:", log)

# =========================
# 🔥 SANITIZAR NOMBRE (SEGURIDAD)
# =========================
def nombre_seguro(nombre):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nombre)

# =========================
# 🔥 GENERADOR SOFTWARE REAL
# =========================
def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

def crear_proyecto(nombre, peso):
    nombre = nombre_seguro(nombre)
    base = f"maia_projects/{nombre}"

    os.makedirs(base, exist_ok=True)

    generar_archivo(f"{base}/flight_controller.py", f"""
class FlightController:
    def __init__(self):
        self.altura = 0
        self.velocidad = 0

    def update(self, thrust, peso):
        g = 9.81
        fuerza = thrust - peso * g
        aceleracion = fuerza / peso
        self.velocidad += aceleracion * 0.1
        self.altura += self.velocidad * 0.1
        return self.altura
""")

    generar_archivo(f"{base}/failsafe.py", """
class FailSafe:
    def check(self, bateria, gps):
        if bateria < 20:
            return "RETURN_HOME"
        if not gps:
            return "EMERGENCY_LAND"
        return "OK"
""")

    generar_archivo(f"{base}/main.py", f"""
from flight_controller import FlightController
from failsafe import FailSafe

fc = FlightController()
fs = FailSafe()

peso = {peso}
thrust = peso * 2

for i in range(50):
    altura = fc.update(thrust, peso)
    estado = fs.check(100, True)
    print(f"Altura: {{altura:.2f}} | Estado: {{estado}}")
""")

    return base

# =========================
# 🧠 CORE
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        with lock_maia:
            estado_maia["progreso"] = val
            estado_maia["mensaje"] = msg
            estado_maia["estado"] = "PROCESANDO"
        log_event("PROGRESO", f"{val}% - {msg}")
        time.sleep(0.3)

    def analizar(self, idea):
        self.progreso(10, "Analizando idea")

        idea = idea.lower()
        peso = 5
        tipo = "general"

        if "incendio" in idea:
            peso = 12
            tipo = "emergencia"
        elif "seguridad" in idea:
            peso = 6
            tipo = "vigilancia"

        return {"peso": peso, "tipo": tipo}

    def ejecutar(self, idea):
        try:
            with lock_maia:
                estado_maia["estado"] = "INICIANDO"

            analisis = self.analizar(idea)

            self.progreso(40, "Generando software real")

            nombre = f"drone_{int(time.time())}"
            ruta = crear_proyecto(nombre, analisis["peso"])

            self.progreso(70, "Simulando")

            altura = analisis["peso"] * 0.5

            self.progreso(100, "Completado")

            with lock_maia:
                estado_maia["estado"] = "COMPLETADO"

            return {
                "viabilidad": "VIABLE ✅",
                "analisis": analisis,
                "software_generado": ruta,
                "simulacion": {
                    "altura_estimada": altura
                }
            }

        except Exception as e:
            with lock_maia:
                estado_maia["estado"] = "ERROR"
                estado_maia["mensaje"] = str(e)

            log_event("ERROR", str(e))

            return {
                "viabilidad": "ERROR ❌",
                "error": str(e)
            }

# =========================
# 🚀 PROCESO ASÍNCRONO
# =========================
def proceso_maia(idea):
    global resultado_global

    core = MaiaCore()
    resultado = core.ejecutar(idea)

    with lock_maia:
        resultado_global = resultado

# =========================
# 🚀 ENDPOINTS
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    if len(idea.strip()) < 5:
        return jsonify({"error": "Idea insuficiente"})

    hilo = threading.Thread(target=proceso_maia, args=(idea,))
    hilo.start()

    return jsonify({"status": "procesando"})

@app.route("/maia_progreso")
def maia_progreso():
    with lock_maia:
        return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    with lock_maia:
        return jsonify(resultado_global)

# =========================
# 🔥 3D
# =========================
@app.route("/generar_3d", methods=["POST"])
def generar_3d():
    if not trimesh:
        return jsonify({"modelo_url": "/static/no_3d.txt"})

    cuerpo = trimesh.creation.box(extents=(0.4, 0.4, 0.08))

    os.makedirs("static", exist_ok=True)
    ruta = "static/modelo_drone.glb"
    cuerpo.export(ruta)

    return jsonify({"modelo_url": "/" + ruta})

# =========================
# 🔥 VISTAS
# =========================
@app.route("/maia_panel")
def maia_panel():
    return render_template("maia_panel.html")

@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/maia_lab")
def maia_lab():
    return render_template("maia_lab.html")

@app.route("/maia_simulador")
def maia_simulador():
    return render_template("maia_simulador.html")

@app.route("/maia_architect")
def maia_architect():
    return render_template("maia_architect.html")

# =========================
# RESTO
# =========================
@app.route("/ping")
def ping():
    return "OK"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    return jsonify([])

@app.route("/maia_chat")
def maia_chat():
    return render_template("maia_chat.html")

@app.route("/drones/<drone_file>")
def abrir_drone(drone_file):
    ruta_html = f"drones/{drone_file}.html"
    if os.path.exists(os.path.join(app.template_folder, ruta_html)):
        return render_template(ruta_html)
    return "Drone no encontrado", 404

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)