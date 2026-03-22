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
# 🔥 ESTADO GLOBAL (PROGRESO)
# =========================
estado_maia = {
    "progreso": 0,
    "estado": "IDLE",
    "mensaje": ""
}

# =========================
# 🔥 LOGGER EMPRESARIAL
# =========================
def log_event(tipo, mensaje):
    log = {
        "tipo": tipo,
        "mensaje": mensaje,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print("🧠 LOG:", log)

# =========================
# 🔥 CARGA DRONES
# =========================
def cargar_drones_base():
    drones = []
    carpeta_drones = os.path.join(app.template_folder, "drones")

    if not os.path.exists(carpeta_drones):
        return []

    for archivo in os.listdir(carpeta_drones):
        if archivo.endswith(".html"):
            ruta = "/drones/" + archivo.replace(".html", "")
            path_completo = os.path.join(carpeta_drones, archivo)

            try:
                with open(path_completo, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    titulo = soup.title.string.strip() if soup.title else archivo.replace(".html", "")
            except:
                titulo = archivo.replace(".html", "")

            drones.append({
                "nombre": titulo,
                "ruta": ruta,
                "categoria": "industrial"
            })

    return drones

try:
    DRONES_BASE = cargar_drones_base()
except:
    DRONES_BASE = []

# =========================
# 🧠 MEMORIA JSON
# =========================
MEMORIA_PATH = "memoria_maia.json"

def cargar_memoria():
    if not os.path.exists(MEMORIA_PATH):
        return []
    try:
        with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_memoria(data):
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# 🧠 CORE EMPRESARIAL
# =========================
class MaiaCore:

    def actualizar_progreso(self, valor, mensaje):
        estado_maia["progreso"] = valor
        estado_maia["mensaje"] = mensaje
        estado_maia["estado"] = "PROCESANDO"
        log_event("PROGRESO", f"{valor}% - {mensaje}")
        time.sleep(0.4)  # simula trabajo real

    def analizar(self, idea):
        self.actualizar_progreso(10, "Analizando idea")

        idea = idea.lower()
        peso = 5
        tipo = "general"

        if "incendio" in idea:
            peso = 12
            tipo = "emergencia"
        elif "seguridad" in idea:
            peso = 6
            tipo = "vigilancia"

        return {
            "peso": peso,
            "tipo": tipo,
            "empuje_requerido": peso * 2
        }

    def generar_software(self):
        self.actualizar_progreso(30, "Diseñando arquitectura de software")

        return {
            "arquitectura": "ROS2 + PX4 + MAVLink + Microservicios + Edge AI",
            "capas": [
                "Percepción",
                "Fusión de sensores",
                "Planificación",
                "Control",
                "Failsafe",
                "Telemetría"
            ],
            "modulos": [
                "flight_controller.py",
                "navigation.py",
                "vision_ai.py",
                "state_estimator.py",
                "failsafe.py",
                "mission_manager.py",
                "telemetry_stream.py"
            ],
            "algoritmos": [
                "PID",
                "Kalman",
                "SLAM",
                "A*",
                "Sensor Fusion",
                "CNN"
            ],
            "failsafe": [
                "Return Home",
                "Auto Landing",
                "Motor Cutoff",
                "GPS Recovery"
            ]
        }

    def generar_hardware(self, peso):
        self.actualizar_progreso(50, "Seleccionando hardware")

        return [
            "Frame carbono industrial",
            "4x Motores brushless",
            "ESC 40A",
            "Pixhawk Cube",
            "GPS Ublox",
            "Lidar",
            "Cámara HD",
            "Batería LiPo 6S"
        ]

    def simular(self, peso):
        self.actualizar_progreso(70, "Simulando física de vuelo")

        dt = 0.05
        altura = 0
        velocidad = 0
        empuje = peso * 2
        g = 9.81

        for _ in range(80):
            fuerza = empuje - peso * g
            aceleracion = fuerza / peso
            velocidad += aceleracion * dt
            altura += velocidad * dt

        return {
            "altura_final": round(altura, 2),
            "estado": "ESTABLE ✅" if altura > 1 else "INESTABLE ⚠️"
        }

    def ejecutar(self, idea):
        estado_maia["estado"] = "INICIANDO"

        analisis = self.analizar(idea)
        software = self.generar_software()
        hardware = self.generar_hardware(analisis["peso"])
        simulacion = self.simular(analisis["peso"])

        self.actualizar_progreso(100, "Drone completado")

        estado_maia["estado"] = "COMPLETADO"

        return {
            "viabilidad": "VIABLE ✅",
            "analisis": analisis,
            "software": software,
            "hardware": hardware,
            "simulacion": simulacion
        }

# =========================
# 🚀 EJECUCIÓN ASÍNCRONA
# =========================
resultado_global = {}

def proceso_maia(idea):
    global resultado_global
    core = MaiaCore()
    resultado_global = core.ejecutar(idea)

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
    return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

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
# 🔥 PANEL
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
    return jsonify(DRONES_BASE)

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