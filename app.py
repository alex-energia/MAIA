from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
import os
import time
import zipfile
import threading

print("🔥 MAIA ULTRA STARTING...")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

# 🔥 ANTI CACHE
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# INIT
init_db()
app.register_blueprint(proyectos_bp)

estado_maia = {"progreso": 0, "estado": "IDLE", "mensaje": ""}
resultado_global = {}

# =========================
# UTILIDADES
# =========================
def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

# =========================
# SOFTWARE INDUSTRIAL REAL
# =========================
def generar_software(base):

    software_path = os.path.join(base, "software")
    os.makedirs(software_path, exist_ok=True)

    archivos = {

        "main.py": """from control.flight_controller import FlightController
from navigation.pathfinding import Pathfinder
from vision.fire_detection import FireDetector
from failsafe.system import FailSafe

def main():
    fc = FlightController()
    nav = Pathfinder()
    vision = FireDetector()
    fs = FailSafe()

    while True:
        estado = fc.update()
        ruta = nav.compute()
        fuego = vision.detect()

        if fs.check():
            fc.return_home()

if __name__ == "__main__":
    main()
""",

        "control/flight_controller.py": """class FlightController:

    def __init__(self):
        self.kp = 1.2
        self.ki = 0.01
        self.kd = 0.5
        self.integral = 0
        self.prev_error = 0

    def pid(self, setpoint, measured, dt):
        error = setpoint - measured
        self.integral += error * dt
        deriv = (error - self.prev_error) / dt

        output = self.kp*error + self.ki*self.integral + self.kd*deriv
        self.prev_error = error

        return output

    def update(self):
        return "control actualizado"

    def return_home(self):
        print("Returning to base")
""",

        "navigation/pathfinding.py": """import heapq

class Pathfinder:

    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def compute(self):
        return "ruta generada"
""",

        "vision/fire_detection.py": """class FireDetector:

    def detect(self):
        return False
""",

        "failsafe/system.py": """class FailSafe:

    def check(self):
        return False
"""
    }

    for nombre, contenido in archivos.items():
        ruta = os.path.join(software_path, nombre)
        generar_archivo(ruta, contenido)

    return archivos

# =========================
# MODELO 3D
# =========================
def generar_modelo_3d(base, peso):
    path = os.path.join(base, "models")
    os.makedirs(path, exist_ok=True)

    escala = max(1, peso / 3)

    partes = {
        "frame.obj": f"o frame\nv {-escala} 0 {-escala}\nv {escala} 0 {-escala}\nv {escala} 0 {escala}\nv {-escala} 0 {escala}",
        "arm_x.obj": f"o arm\nv {-escala} 0 0\nv {escala} 0 0",
        "arm_z.obj": f"o arm\nv 0 0 {-escala}\nv 0 0 {escala}",
    }

    for n, c in partes.items():
        generar_archivo(os.path.join(path, n), c)

    return {
        "componentes": list(partes.keys()),
        "escala": escala
    }

# =========================
# ZIP
# =========================
def exportar_zip(ruta):
    if not os.path.exists(ruta):
        return ""

    zip_path = ruta + ".zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(ruta):
            for file in files:
                full = os.path.join(root, file)
                zipf.write(full, os.path.relpath(full, ruta))

    return zip_path

# =========================
# CORE
# =========================
class MaiaCore:

    def ejecutar_paso(self, idea, paso, data):

        print(f"➡️ Paso {paso}")

        if paso == 0:
            core = analizar_drone(idea)
            return {"paso": 1, "data": {"core": core}}

        elif paso == 1:
            analisis = data.get("core", {}).get("analisis", {})
            peso = analisis.get("peso", 10)

            data["analisis_pro"] = {
                **analisis,
                "estructura": "Fibra de carbono reforzada",
                "nivel_autonomia": "Alto",
                "carga_util_kg": round(peso * 0.4, 2)
            }

            data["hardware"] = {
                "frame": "Fibra de carbono",
                "motores": "Brushless 1200kv x4",
                "bateria": "LiPo 6S 10000mAh",
                "sensores": ["térmico", "humo", "GPS", "IMU"]
            }

            data["bom"] = [
                "4x motores brushless",
                "flight controller",
                "batería LiPo",
                "ESC",
                "GPS",
                "sensor térmico"
            ]

            return {"paso": 2, "data": data}

        elif paso == 2:
            base = f"maia_projects/{int(time.time())}"
            os.makedirs(base, exist_ok=True)
            data["base"] = base

            data["software"] = generar_software(base)

            return {"paso": 3, "data": data}

        elif paso == 3:
            data["fisica"] = {
                "empuje": 250,
                "autonomia": 45,
                "consumo": "alto"
            }
            return {"paso": 4, "data": data}

        elif paso == 4:
            data["riesgos"] = [
                "viento extremo",
                "sobrecalentamiento",
                "fallo batería",
                "interferencia señal"
            ]
            return {"paso": 5, "data": data}

        elif paso == 5:
            peso = data.get("analisis_pro", {}).get("peso", 10)
            data["modelos_3d"] = generar_modelo_3d(data["base"], peso)
            return {"paso": 6, "data": data}

        elif paso == 6:
            data["zip"] = exportar_zip(data["base"])
            return {"final": True, "resultado": data}

# =========================
# ENDPOINTS
# =========================
@app.route("/maia_step", methods=["POST"])
def maia_step():
    req = request.get_json() or {}
    idea = req.get("idea", "")
    paso = int(req.get("paso", 0))
    data = req.get("data", {})

    core = MaiaCore()
    resultado = core.ejecutar_paso(idea, paso, data)

    return jsonify(resultado)

# =========================
# VISTAS
# =========================
@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)