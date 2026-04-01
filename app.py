from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone

import os
import time
import zipfile
import math

print("🔥 MAIA INDUSTRIAL CORE V3")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

# =========================
# 🔥 NO CACHE
# =========================
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

init_db()
app.register_blueprint(proyectos_bp)

# =========================
# 📁 UTIL
# =========================
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# =========================
# 🧠 SOFTWARE INDUSTRIAL
# =========================
def generar_software(base):
    path = os.path.join(base, "software")

    archivos = {

# ================= MAIN =================
"main.py": """from control.flight_controller import FlightController
from navigation.astar import AStar
from perception.fire import FireDetector
from systems.failsafe import FailSafe

def main():
    fc = FlightController()
    nav = AStar()
    vision = FireDetector()
    fs = FailSafe()

    while True:
        sensors = {
            "altitude": 12,
            "roll": 0.2,
            "pitch": -0.1
        }

        control = fc.update(sensors, 0.02)
        path = nav.find_path((0,0), (10,10))
        fire = vision.detect(80)

        if fs.check(18, True) != "OK":
            fc.return_home()

if __name__ == "__main__":
    main()
""",

# ================= PID =================
"control/pid.py": """class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0

    def update(self, setpoint, measured, dt):
        error = setpoint - measured
        self.integral += error * dt
        deriv = (error - self.prev_error) / dt

        output = self.kp*error + self.ki*self.integral + self.kd*deriv
        self.prev_error = error
        return output
""",

# ================= CONTROL =================
"control/flight_controller.py": """from control.pid import PID

class FlightController:
    def __init__(self):
        self.alt = PID(1.2, 0.01, 0.4)
        self.roll = PID(0.8, 0.02, 0.3)
        self.pitch = PID(0.8, 0.02, 0.3)

    def update(self, sensors, dt):
        return {
            "throttle": self.alt.update(10, sensors["altitude"], dt),
            "roll": self.roll.update(0, sensors["roll"], dt),
            "pitch": self.pitch.update(0, sensors["pitch"], dt)
        }

    def return_home(self):
        print("🚨 RETURN HOME")
""",

# ================= NAV =================
"navigation/astar.py": """import heapq

class AStar:
    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def find_path(self, start, goal):
        open_set = [(0, start)]
        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return ["ruta encontrada"]

            visited.add(current)

            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                neighbor = (current[0]+dx, current[1]+dy)

                if neighbor in visited:
                    continue

                priority = self.heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))

        return []
""",

# ================= VISION =================
"perception/fire.py": """class FireDetector:
    def detect(self, temp):
        if temp > 70:
            return {"fire": True, "confidence": 0.95}
        return {"fire": False}
""",

# ================= FAILSAFE =================
"systems/failsafe.py": """class FailSafe:
    def check(self, battery, signal):
        if battery < 20:
            return "LOW_BATTERY"
        if not signal:
            return "SIGNAL_LOSS"
        return "OK"
"""
    }

    for name, content in archivos.items():
        write_file(os.path.join(path, name), content)

    return archivos

# =========================
# ⚙️ FÍSICA REAL
# =========================
def calcular_fisica(peso_kg, motores=4):
    thrust_por_motor = 6.5  # kg empuje
    thrust_total = motores * thrust_por_motor
    peso_total = peso_kg * 9.81

    relacion = thrust_total / peso_kg

    estado = "INESTABLE"
    if thrust_total > peso_kg * 2:
        estado = "ESTABLE"

    return {
        "thrust_total_kg": thrust_total,
        "peso_total_n": round(peso_total, 2),
        "relacion_empuje_peso": round(relacion, 2),
        "estado_vuelo": estado,
        "autonomia_estimada_min": round(40 - peso_kg * 0.5, 2)
    }

# =========================
# 🔩 HARDWARE REAL
# =========================
def generar_hardware(peso):
    return {
        "estructura": "carbon fiber aerospace",
        "propulsion": {
            "motor_kv": 1200,
            "thrust_por_motor_kg": 6.5,
            "total_motores": 4
        },
        "energia": {
            "bateria": "LiPo 6S 10000mAh",
            "voltaje": 22.2
        },
        "sensores": [
            "thermal",
            "lidar",
            "gps",
            "imu"
        ],
        "peso_total": peso
    }

# =========================
# 🧱 MODELO 3D MEJORADO
# =========================
def generar_modelo_3d(base, peso):
    path = os.path.join(base, "models")
    os.makedirs(path, exist_ok=True)

    escala = peso / 2

    write_file(os.path.join(path, "frame.obj"),
f"""o frame
v {-escala} 0 {-escala}
v {escala} 0 {-escala}
v {escala} 0 {escala}
v {-escala} 0 {escala}
""")

    write_file(os.path.join(path, "motor.obj"),
f"""o motor
v 0 0 0
v 0 {escala} 0
""")

    return {
        "tipo": "quad_x",
        "escala": escala,
        "componentes": ["frame", "motor x4"]
    }

# =========================
# 📦 ZIP
# =========================
def exportar_zip(path):
    zip_path = path + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(path):
            for file in files:
                full = os.path.join(root, file)
                zipf.write(full, os.path.relpath(full, path))
    return zip_path

# =========================
# 🧠 CORE
# =========================
class MaiaCore:

    def ejecutar_paso(self, idea, paso, data):

        print("➡️ Paso", paso)

        if paso == 0:
            core = analizar_drone(idea)
            return {"paso": 1, "data": {"core": core}}

        elif paso == 1:
            analisis = data["core"].get("analisis", {})
            peso = analisis.get("peso", 12)

            data["hardware"] = generar_hardware(peso)
            data["analisis_pro"] = analisis

            return {"paso": 2, "data": data}

        elif paso == 2:
            base = f"maia_projects/{int(time.time())}"
            os.makedirs(base, exist_ok=True)

            data["base"] = base
            data["software"] = generar_software(base)

            return {"paso": 3, "data": data}

        elif paso == 3:
            peso = data["hardware"]["peso_total"]
            data["fisica"] = calcular_fisica(peso)

            return {"paso": 4, "data": data}

        elif paso == 4:
            data["riesgos"] = [
                "viento extremo",
                "sobrecarga térmica",
                "fallo batería",
                "pérdida señal"
            ]
            return {"paso": 5, "data": data}

        elif paso == 5:
            peso = data["hardware"]["peso_total"]
            data["modelos_3d"] = generar_modelo_3d(data["base"], peso)

            return {"paso": 6, "data": data}

        elif paso == 6:
            data["zip"] = exportar_zip(data["base"])
            return {"final": True, "resultado": data}

# =========================
# API
# =========================
@app.route("/maia_step", methods=["POST"])
def maia_step():
    req = request.get_json() or {}

    idea = req.get("idea", "")
    paso = int(req.get("paso", 0))
    data = req.get("data", {})

    core = MaiaCore()
    return jsonify(core.ejecutar_paso(idea, paso, data))

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
    app.run(host="0.0.0.0", port=10000)