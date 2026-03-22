from flask import Flask, render_template, request, jsonify, session
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
import math
import numpy as np

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

            categoria = "industrial"
            drones.append({
                "nombre": titulo,
                "ruta": ruta,
                "categoria": categoria
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

    def analizar(self, idea):
        idea = idea.lower()
        peso = 5
        tipo = "general"

        if "incendio" in idea:
            peso = 12
            tipo = "emergencia"
        elif "seguridad" in idea:
            peso = 6
            tipo = "vigilancia"

        empuje = peso * 2

        log_event("ANALISIS", f"Tipo: {tipo}, Peso: {peso}")

        return {
            "peso": peso,
            "tipo": tipo,
            "empuje_requerido": empuje
        }

    # 🔥 SOFTWARE NIVEL INDUSTRIA
    def generar_software(self):
        return {
            "arquitectura": "ROS2 + PX4 + MAVLink + Microservicios",
            "capas": [
                "Percepción",
                "Planificación",
                "Control",
                "Comunicación",
                "Seguridad"
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
                "PID Control",
                "Kalman Filter",
                "SLAM",
                "A* Pathfinding",
                "Sensor Fusion",
                "Computer Vision CNN"
            ],
            "failsafe": [
                "Return To Home",
                "Auto Landing",
                "Motor Cutoff",
                "Signal Loss Recovery"
            ]
        }

    def generar_hardware(self, peso):
        return [
            "Frame carbono industrial",
            "4x Motores brushless",
            "ESC 40A",
            "Pixhawk Cube",
            "GPS Ublox M8N",
            "Lidar",
            "Cámara HD",
            "Batería LiPo 6S"
        ]

    # 🔥 SIMULACIÓN PROFESIONAL (TIEMPO REAL)
    def simular(self, peso):
        dt = 0.05
        altura = 0
        velocidad = 0
        empuje = peso * 2
        g = 9.81

        historial = []

        for t in range(100):
            fuerza = empuje - peso * g
            aceleracion = fuerza / peso

            velocidad += aceleracion * dt
            altura += velocidad * dt

            historial.append({
                "t": t,
                "altura": round(altura, 2),
                "velocidad": round(velocidad, 2),
                "aceleracion": round(aceleracion, 2)
            })

        estabilidad = max(h["altura"] for h in historial) - min(h["altura"] for h in historial)

        estado = "ESTABLE ✅" if estabilidad < 5 else "INESTABLE ⚠️"

        return {
            "estado": estado,
            "historial": historial,
            "altura_final": round(altura, 2),
            "estabilidad": round(estabilidad, 2)
        }

    def ejecutar(self, idea):
        analisis = self.analizar(idea)

        resultado = {
            "viabilidad": "VIABLE ✅",
            "analisis": analisis,
            "software": self.generar_software(),
            "hardware": self.generar_hardware(analisis["peso"]),
            "simulacion": self.simular(analisis["peso"])
        }

        log_event("RESULTADO", "Drone generado correctamente")

        return resultado

# =========================
# 🔥 MODELO 3D
# =========================
def generar_modelo_3d(_):
    if not trimesh:
        return "/static/no_3d.txt"

    cuerpo = trimesh.creation.box(extents=(0.4, 0.4, 0.08))

    drone = trimesh.util.concatenate([cuerpo])

    os.makedirs("static", exist_ok=True)
    ruta = "static/modelo_drone.glb"
    drone.export(ruta)

    return "/" + ruta

# =========================
# 🚀 ENDPOINTS
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    if len(idea.strip()) < 5:
        return jsonify({
            "viabilidad": "NO VIABLE ❌",
            "causas": ["Idea poco definida"]
        })

    core = MaiaCore()
    return jsonify(core.ejecutar(idea))

@app.route("/generar_3d", methods=["POST"])
def generar_3d():
    return jsonify({
        "modelo_url": generar_modelo_3d({})
    })

# =========================
# 🔥 PANEL PROFESIONAL
# =========================
@app.route("/maia_panel")
def maia_panel():
    return render_template("maia_panel.html")

# =========================
# 🔥 RUTAS
# =========================
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